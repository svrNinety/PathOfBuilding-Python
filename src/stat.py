from enum import Enum


class StatType(str, Enum):
    Base = "base"
    Increased = "increased"
    More = "more"


class Stat(str, Enum):
    def __init__(self, value: str, *args, **kwargs):
        if any(value == other.value for other in self.__class__):
            raise RuntimeError("member already exists")
        super().__init__(*args, **kwargs)

    Strength = "strength"
    Dexterity = "dexterity"
    Intelligence = "intelligence"
    Life = "life"
    EnergyShield = "energy_shield"
    Armour = "armour"
    EvasionRating = "evasion_rating"
    SpellDamage = "spell_damage"
    SpellMinimumBaseFireDamage = "spell_minimum_base_fire_damage"
    SpellMaximumBaseFireDamage = "spell_maximum_base_fire_damage"
    SpellBaseFireDamageMaximumLife = "spell_base_fire_damage_%_maximum_life"



if __name__ == '__main__':
    print(Stat.Strength)
