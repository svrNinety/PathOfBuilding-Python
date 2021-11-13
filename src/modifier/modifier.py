import re
from enum import Enum
from typing import Any, Type

import parse
from modifier_enum import (
    ConditionalValueModifierEnum,
    DynamicValueModifierEnum,
    ValueModifierEnum,
)
from modifier_mixin import (
    ConditionalModifierMixin,
    DynamicValueModifierMixin,
    ModifierMixin,
    ValueModifierMixin,
)


class Modifier(ModifierMixin):
    pass


class ValueModifier(ModifierMixin, ValueModifierMixin):
    pass


class ConditionalValueModifier(
    ModifierMixin, ValueModifierMixin, ConditionalModifierMixin
):
    pass


class DynamicValueModifier(ModifierMixin, DynamicValueModifierMixin):
    pass


def _infer_modifier_type_from_text(
    modifier_text: str,
) -> tuple[Type[ModifierMixin], Type[Enum], Any]:
    for _cls, _enum in zip(
        [ValueModifier, DynamicValueModifier, ConditionalValueModifier],
        [ValueModifierEnum, DynamicValueModifierEnum, ConditionalValueModifierEnum],
    ):
        for _member in _enum:
            res = re.search(pattern=_member.value["regexp"], string=modifier_text)
            if res:
                return _cls, _enum, _member.value
    raise RuntimeError(f"Modifier '{modifier_text}' couldn't be matched")


def _instantiate_modifier_instance_from_text(modifier_text: str) -> ModifierMixin:
    cls, modifier_type, type_requirements = _infer_modifier_type_from_text(
        modifier_text=modifier_text
    )
    params = parse.parse(format=type_requirements["fmt"], string=modifier_text).named
    kwargs = params | type_requirements
    return cls(**kwargs)


if __name__ == "__main__":
    m = Modifier.from_text("3% more Spell Damage per Power Charge")
    m2 = Modifier.from_text("2% more Spell Damage per Power Charge")
    m3 = m + m2
    print(m.text)
    print(m2.text)
    print(m3.text)
    s = sum([m, m2, m3])
    print(s.text)
