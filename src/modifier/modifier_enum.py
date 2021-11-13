from enum import Enum

from src.stat import Stat, StatType

""" classification and definition of all modifiers """

_INT = r"[-+]?[0-9]*"
_FLOAT = r"[-+]?[0-9]*\.[0-9]+"


class ValueModifierEnum(Enum):
    MoreSpellDamage = dict(
        identifier="more_spell_damage",
        regexp=f"^{_INT}% more Spell Damage$",
        fmt="{value:d}% more Spell Damage",
        targets=[Stat.SpellDamage],
        kind=StatType.More,
    )
    AdditionalStrength = dict(
        identifier="additional_strength",
        regexp=f"^\+{_INT} to Strength$",
        fmt="+{value:d} to Strength",
        targets=[Stat.Strength],
        kind=StatType.Base,
    )
    IncreasedStrength = dict(
        identifier="increased_strength",
        regexp=f"^{_INT}% increased Strength$",
        fmt="{value:d}% increased Strength",
        targets=[Stat.Strength],
        kind=StatType.Increased,
    )
    MoreStrength = dict(
        identifier="more_strength",
        regexp=f"^{_INT}% more Strength$",
        fmt="{value:d}% more Strength",
        targets=[Stat.Strength],
        kind=StatType.More,
    )
    IncreasedSpellDamage = dict(
        identifier="increased_spell_damage",
        regexp=f"^{_INT}% increased Spell Damage$",
        fmt="{value:d}% increased Spell Damage",
        targets=[Stat.SpellDamage],
        kind=StatType.Increased,
    )


class DynamicValueModifierEnum(Enum):
    IncreasedSpellDamage = dict(
        identifier="more_spell_damage_per_power_charge",
        regexp=f"^{_INT}% more Spell Damage per Power Charge$",
        fmt="{value:d}% more Spell Damage per Power Charge",
        targets=[Stat.SpellDamage],
        kind=StatType.Increased,
        scaler=lambda: 5,
    )


class ConditionalValueModifierEnum(Enum):
    IncreasedSpellDamageWhileHoldingAShield = dict(
        identifier="increased_spell_damage_while_holding_a_shield",
        regexp=f"^{_INT}% increased Spell Damage while holding a Shield$",
        fmt="{value:d}% increased Spell Damage while holding a Shield",
        targets=[Stat.SpellDamage],
        kind=StatType.Increased,
        predicates=[lambda: True],
    )
