from dataclasses import dataclass
from typing import List

from models.dt_value import DTModifierDict


@dataclass
class SavingThrowsModifier:
    STR: List[DTModifierDict]
    DEX: List[DTModifierDict]
    CON: List[DTModifierDict]
    INT: List[DTModifierDict]
    WIS: List[DTModifierDict]
    CHA: List[DTModifierDict]
