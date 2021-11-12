import re
from enum import Enum
from functools import cached_property
from numbers import Integral, Real
from typing import Any, Callable, Iterable, Type, Union

import parse
from modifier_enum import ConditionalValueModifierEnum, ValueModifierEnum


def _infer_modifier_type_from_text(modifier_text: str) -> tuple[Type["Modifier"], Type[Enum], Any]:
    for _cls, _enum in zip(
        [ValueModifier, ConditionalValueModifier], [ValueModifierEnum, ConditionalValueModifierEnum]
    ):
        for _member in _enum:
            res = re.search(pattern=_member.value["regexp"], string=modifier_text)
            if res:
                return _cls, _enum, _member.value
    raise RuntimeError(f"Modifier '{modifier_text}' couldn't be matched")


def _parse_modifier_parameters_from_text(fmt: str, modifier_text: str) -> dict[str, Any]:
    return parse.parse(format=fmt, string=modifier_text).named


def _instantiate_modifier_instance_from_text(modifier_text: str) -> "Modifier":
    cls, modifier_type, type_requirements = _infer_modifier_type_from_text(modifier_text=modifier_text)
    params = _parse_modifier_parameters_from_text(fmt=type_requirements["fmt"], modifier_text=modifier_text)
    if modifier_type == ValueModifierEnum:
        cls = ValueModifier
    elif modifier_type == ConditionalValueModifierEnum:
        cls = ConditionalValueModifier
    kwargs = params | type_requirements
    return cls(**kwargs)


class Modifier:
    def __init__(self, identifier: str, regexp: str, fmt: str, *args, **kwargs):
        self._identifier: str = identifier
        self._regexp: str = regexp
        self._fmt: str = fmt
        super(Modifier, self).__init__(*args, **kwargs)  # type: ignore

    @classmethod
    def from_text(cls, modifier_text: str) -> "Modifier":
        return _instantiate_modifier_instance_from_text(modifier_text=modifier_text)

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def regexp(self) -> str:
        return self._regexp

    @property
    def fmt(self) -> str:
        return self._fmt

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.__dict__!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Modifier):
            return self._identifier == other._identifier
        return False


class ConditionalModifierMixin:
    def __init__(self, predicates, *args, **kwargs):
        self._predicates = predicates
        super(ConditionalModifierMixin, self).__init__(*args, **kwargs)

    @property
    def predicates(self) -> Iterable[Callable[[], bool]]:
        return self._predicates

    @cached_property
    def text(self) -> str:
        return self.fmt.format()  # type: ignore


class ValueModifierMixin:
    def __init__(self, value, *args, **kwargs):
        self._value = value
        super(ValueModifierMixin, self).__init__(*args, **kwargs)

    @property
    def value(self):
        return self._value

    @cached_property
    def text(self) -> str:
        return self.fmt.format(value=self.value)  # type: ignore

    def __add__(self, other: "ValueModifierMixin") -> "Modifier":
        assert self == other, f"modifier mismatch"
        _text = self.fmt.format(value=self.value + other.value)  # type: ignore
        return Modifier.from_text(_text)

    def __sub__(self, other: "ValueModifierMixin") -> "Modifier":
        assert self == other, f"modifier mismatch"
        _text = self.fmt.format(value=self.value - other.value)  # type: ignore
        return Modifier.from_text(_text)

    def __mul__(self, other: Union["ValueModifierMixin", Integral, Real]) -> "Modifier":
        if isinstance(other, ValueModifierMixin):
            assert self == other, f"modifier mismatch"
            other = other.value
        _text = self.fmt.format(value=self.value * other)  # type: ignore
        return Modifier.from_text(_text)

    def __radd__(self, other):
        _text = self.fmt.format(value=other.value + self.value)  # type: ignore
        return Modifier.from_text(_text)

    def __rmul__(self, other: Union["ValueModifierMixin", Integral, Real]) -> "Modifier":
        if isinstance(other, ValueModifierMixin):
            assert self == other, f"modifier mismatch"
            other = other.value
        _text = self.fmt.format(value=other * self.value)  # type: ignore
        return Modifier.from_text(_text)

    def __iadd__(self, other: "ValueModifierMixin") -> "ValueModifierMixin":
        assert self == other, f"modifier mismatch"
        self._value += other.value
        return self

    def __isub__(self, other: "ValueModifierMixin") -> "ValueModifierMixin":
        assert self == other, f"modifier mismatch"
        self._value -= other.value
        return self

    def __imul__(self, other: Union["ValueModifierMixin", Integral, Real]) -> "ValueModifierMixin":
        if isinstance(other, ValueModifierMixin):
            assert self == other, f"modifier mismatch"
            other = other.value
        self._value *= other
        return self


class ValueModifier(Modifier, ValueModifierMixin):
    pass


class ConditionalValueModifier(Modifier, ConditionalModifierMixin, ValueModifierMixin):
    pass


if __name__ == "__main__":
    a = Modifier.from_text("+20 to Strength")
    b = Modifier.from_text("+15 to Strength")
    print(a)
    print(b)
    print(a + b)
    print(a - b)
    print(a * 3)
    print(4 * a)
    m = Modifier.from_text("15% increased Spell Damage while holding a Shield")
    print(m)
    print(m * 3)
