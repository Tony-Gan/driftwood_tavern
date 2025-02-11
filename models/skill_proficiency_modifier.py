from dataclasses import dataclass
from typing import List

from models.dt_value import DTModifierDict


@dataclass
class SkillProficiencyModifier:
    acrobatics: List[DTModifierDict]
    animal_handling: List[DTModifierDict]
    arcana: List[DTModifierDict]
    athletics: List[DTModifierDict]
    deception: List[DTModifierDict]
    history: List[DTModifierDict]
    insight: List[DTModifierDict]
    intimidation: List[DTModifierDict]
    investigation: List[DTModifierDict]
    medicine: List[DTModifierDict]
    nature: List[DTModifierDict]
    perception: List[DTModifierDict]
    performance: List[DTModifierDict]
    persuasion: List[DTModifierDict]
    religion: List[DTModifierDict]
    sleight_of_hand: List[DTModifierDict]
    stealth: List[DTModifierDict]
    survival: List[DTModifierDict]
