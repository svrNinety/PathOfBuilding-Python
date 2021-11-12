import re
from enum import Enum
from typing import Any, Type

import parse
from modifier_enum import ConditionalValueModifierEnum, ValueModifierEnum
from modifier_mixin import ConditionalModifierMixin, Modifier, ValueModifierMixin


class ValueModifier(Modifier, ValueModifierMixin):
    pass


class ConditionalValueModifier(Modifier, ConditionalModifierMixin, ValueModifierMixin):
    pass


def _infer_modifier_type_from_text(modifier_text: str) -> tuple[Type[Modifier], Type[Enum], Any]:
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


def _instantiate_modifier_instance_from_text(modifier_text: str) -> Modifier:
    cls, modifier_type, type_requirements = _infer_modifier_type_from_text(modifier_text=modifier_text)
    params = _parse_modifier_parameters_from_text(fmt=type_requirements["fmt"], modifier_text=modifier_text)
    if modifier_type == ValueModifierEnum:
        cls = ValueModifier
    elif modifier_type == ConditionalValueModifierEnum:
        cls = ConditionalValueModifier
    kwargs = params | type_requirements
    return cls(**kwargs)


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