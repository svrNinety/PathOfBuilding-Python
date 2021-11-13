from __future__ import annotations

from typing import Callable, Iterable, Union


class ModifierMixin:
    def __init__(self, identifier: str, regexp: str, fmt: str, targets, kind, *args, **kwargs):
        self._identifier: str = identifier
        self._regexp: str = regexp
        self._fmt: str = fmt
        super(ModifierMixin, self).__init__(*args, **kwargs)  # type: ignore

    @classmethod
    def from_text(cls, modifier_text: str) -> ModifierMixin:
        from modifier import _instantiate_modifier_instance_from_text

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
        if isinstance(other, ModifierMixin):
            return self._identifier == other._identifier
        return False


class ConditionalModifierMixin:
    def __init__(self, predicates: Iterable[Callable[[], bool]], *args, **kwargs):
        self._predicates: Iterable[Callable[[], bool]] = predicates
        super(ConditionalModifierMixin, self).__init__(*args, **kwargs)  # type: ignore

    @property
    def predicates(self) -> Iterable[Callable[[], bool]]:
        return self._predicates

    @property
    def text(self) -> str:
        return self.fmt.format()  # type: ignore


class ValueModifierMixin:
    def __init__(self, value: Union[int, float], *args, **kwargs):
        self._value: Union[int, float] = value
        super(ValueModifierMixin, self).__init__(*args, **kwargs)  # type: ignore

    @property
    def value(self) -> Union[int, float]:
        return self._value

    @property
    def text(self) -> str:
        return self.fmt.format(value=self.value)  # type: ignore

    def __add__(self, other: ValueModifierMixin) -> ModifierMixin:
        assert self == other, f"modifier mismatch"
        _text = self.fmt.format(value=self._value + other._value)  # type: ignore
        return ModifierMixin.from_text(_text)

    def __sub__(self, other: ValueModifierMixin) -> ModifierMixin:
        assert self == other, f"modifier mismatch"
        _text = self.fmt.format(value=self._value - other._value)  # type: ignore
        return ModifierMixin.from_text(_text)

    def __mul__(self, other: Union[ValueModifierMixin, int, float]) -> ModifierMixin:
        if isinstance(other, ValueModifierMixin):
            assert self == other, f"modifier mismatch"
            other = other._value
        _text = self.fmt.format(value=self._value * other)  # type: ignore
        return ModifierMixin.from_text(_text)

    def __radd__(self, other: Union[ValueModifierMixin, int, float]) -> ModifierMixin:
        if isinstance(other, ValueModifierMixin):
            assert self == other, f"modifier mismatch"
            other = other._value
        _text = self.fmt.format(value=other + self._value)  # type: ignore
        return ModifierMixin.from_text(_text)

    def __rmul__(self, other: Union[ValueModifierMixin, int, float]) -> ModifierMixin:
        if isinstance(other, ValueModifierMixin):
            assert self == other, f"modifier mismatch"
            other = other._value
        _text = self.fmt.format(value=other * self._value)  # type: ignore
        return ModifierMixin.from_text(_text)

    def __iadd__(self, other: ValueModifierMixin) -> ValueModifierMixin:
        assert self == other, f"modifier mismatch"
        self._value += other._value
        return self

    def __isub__(self, other: ValueModifierMixin) -> ValueModifierMixin:
        assert self == other, f"modifier mismatch"
        self._value -= other._value
        return self

    def __imul__(self, other: Union[ValueModifierMixin, int, float]) -> ValueModifierMixin:
        if isinstance(other, ValueModifierMixin):
            assert self == other, f"modifier mismatch"
            other = other._value
        self._value *= other
        return self


class DynamicValueModifierMixin(ValueModifierMixin):
    def __init__(self, scaler: Callable[[], Union[float, int]], *args, **kwargs):
        self._scaler: Callable[[], Union[float, int]] = scaler
        super(DynamicValueModifierMixin, self).__init__(*args, **kwargs)

    @property
    def value(self) -> Union[int, float]:
        return self._value * self._scaler()  # type: ignore
