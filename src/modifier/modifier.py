import re
from enum import Enum
from typing import Any, Type

import parse
from modifier_enum import ConditionalValueModifierEnum, ValueModifierEnum, DynamicValueModifierEnum
from modifier_mixin import ConditionalModifierMixin, ModifierMixin, ValueModifierMixin, DynamicValueModifierMixin


class Modifier(ModifierMixin):
    pass


class ValueModifier(ModifierMixin, ValueModifierMixin):
    pass


class ConditionalValueModifier(ModifierMixin, ValueModifierMixin, ConditionalModifierMixin):
    pass


class DynamicValueModifier(ModifierMixin, DynamicValueModifierMixin):
    pass


def _infer_modifier_type_from_text(modifier_text: str) -> tuple[Type[ModifierMixin], Type[Enum], Any]:
    for _cls, _enum in zip(
        [ValueModifier, DynamicValueModifier, ConditionalValueModifier], [ValueModifierEnum, DynamicValueModifierEnum, ConditionalValueModifierEnum]
    ):
        for _member in _enum:
            res = re.search(pattern=_member.value["regexp"], string=modifier_text)
            if res:
                return _cls, _enum, _member.value
    raise RuntimeError(f"Modifier '{modifier_text}' couldn't be matched")


def _parse_modifier_parameters_from_text(fmt: str, modifier_text: str) -> dict[str, Any]:
    return parse.parse(format=fmt, string=modifier_text).named


def _instantiate_modifier_instance_from_text(modifier_text: str) -> ModifierMixin:
    cls, modifier_type, type_requirements = _infer_modifier_type_from_text(modifier_text=modifier_text)
    params = _parse_modifier_parameters_from_text(fmt=type_requirements["fmt"], modifier_text=modifier_text)
    if modifier_type == ValueModifierEnum:
        cls = ValueModifier
    elif modifier_type == ConditionalValueModifierEnum:
        cls = ConditionalValueModifier
    kwargs = params | type_requirements
    return cls(**kwargs)


if __name__ == "__main__":
    m = Modifier.from_text("3% more Spell Damage per Power Charge")
    m2 = Modifier.from_text("2% more Spell Damage per Power Charge")
    m3 = m + m2
    print(m.text)
    print(m2.text)
    print(m3.text)
