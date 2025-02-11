from dataclasses import dataclass
from typing import Dict


@dataclass
class DTValue:
    base_value: int = 0
    modi_value: int = 0
    modi_value_source: Dict[str, int]
    cust_value: int = 0
    cust_value_source: Dict[str, int]

    def value(self):
        return self.base_value + self.modi_value + self.cust_value
