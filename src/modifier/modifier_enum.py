from enum import Enum

""" classification and definition of all modifiers """

_INT = r"[-+]?[0-9]*"
_FLOAT = r"[-+]?[0-9]*\.[0-9]+"


class ValueModifierEnum(Enum):
    MoreSpellDamage = dict(
        identifier="more_spell_damage_%",
        regexp=f"^{_INT}% more Spell Damage$",
        fmt="{value:d}% more Spell Damage",
    )
    AdditionalStrength = dict(
        identifier="additional_strength",
        regexp=f"^\+{_INT} to Strength$",
        fmt="+{value:d} to Strength",
    )
    IncreasedStrength = dict(
        identifier="increased_strength_%",
        regexp=f"^{_INT}% increased Strength$",
        fmt="{value:d}% increased Strength",
    )
    MoreStrength = dict(
        identifier="more_strength_%",
        regexp=f"^{_INT}% more Strengt$h",
        fmt="{value:d}% more Strength",
    )
    IncreasedSpellDamage = dict(
        identifier="increased_spell_damage_%",
        regexp=f"^{_INT}% increased Spell Damage$",
        fmt="{value:d}% increased Spell Damage",
    )


class DynamicValueModifierEnum(Enum):
    IncreasedSpellDamage = dict(
        identifier="more_spell_damage_%_per_power_charge",
        regexp=f"^{_INT}% more Spell Damage per Power Charge$",
        fmt="{value:d}% more Spell Damage per Power Charge",
        scaler=lambda: 5
    )


class ConditionalValueModifierEnum(Enum):
    IncreasedSpellDamageWhileHoldingAShield = dict(
        identifier="increased_spell_damage_while_holding_a_shield",
        regexp=f"^{_INT}% increased Spell Damage while holding a Shield$",
        fmt="{value:d}% increased Spell Damage while holding a Shield",
        predicates=[lambda: True],  # functions that return true
    )
