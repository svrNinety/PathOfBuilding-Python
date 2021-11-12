from enum import Enum

""" classification and definition of all modifiers """


class ValueModifierEnum(Enum):
    MoreSpellDamage = dict(
        identifier="more_spell_damage_%",
        regexp="^\+[1-9]\d*% more Spell Damage$",
        fmt="{value:d}% more Spell Damage",
    )
    AdditionalStrength = dict(
        identifier="additional_strength",
        regexp="^\+[1-9]\d* to Strength$",
        fmt="+{value:d} to Strength",
    )
    IncreasedStrength = dict(
        identifier="increased_strength_%",
        regexp="^\+[1-9]\d*% increased Strength$",
        fmt="{value:d}% increased Strength",
    )
    MoreStrength = dict(
        identifier="more_strength_%",
        regexp="^\+[1-9]\d*% more Strengt$h",
        fmt="{value:d}% more Strength",
    )
    IncreasedSpellDamage = dict(
        identifier="increased_spell_damage_%",
        regexp="^\+[1-9]\d*% increased Spell Damage$",
        fmt="{value:d}% increased Spell Damage",
    )


class ConditionalValueModifierEnum(Enum):
    IncreasedSpellDamageWhileHoldingAShield = dict(
        identifier="increased_spell_damage_while_holding_a_shield",
        regexp="^[1-9]\d*% increased Spell Damage while holding a Shield$",
        fmt="{value:d}% increased Spell Damage while holding a Shield",
        predicates=[lambda: True],
    )
