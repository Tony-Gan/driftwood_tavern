from models.ability_scores_modifier import AbilityScoresModifier
from models.saving_throws_modifier import SavingThrowsModifier
from models.skill_proficiency_modifier import SkillProficiencyModifier

class Character:
    def __init__(self):
        self.name = ""
        self.level = 0
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0
        
        self.cl = ""
        self.species = ""
        
        self.spells = []
        
        self.ability_scores_modifier = AbilityScoresModifier(
            STR=[], DEX=[], CON=[], INT=[], WIS=[], CHA=[]
        )

        self.saving_throws_modifier = SavingThrowsModifier(
            STR=[], DEX=[], CON=[], INT=[], WIS=[], CHA=[]
        )

        self.skill_proficiency_modifier = SkillProficiencyModifier(
            acrobatics=[], animal_handling=[], arcana=[], athletics=[],
            deception=[], history=[], insight=[], intimidation=[],
            investigation=[], medicine=[], nature=[], perception=[],
            performance=[], persuasion=[], religion=[], sleight_of_hand=[],
            stealth=[], survival=[]
        )
