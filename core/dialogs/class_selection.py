from PyQt6.QtWidgets import QHBoxLayout, QLabel, QTextBrowser, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from ui.dt_base_dialog import DTBaseDialog
from ui.dt_base_frame import DTBaseFrame
from ui.dt_expandable_ticket import DTExpandableTicket
from ui.dt_label import DTNormalLabel, DTSubLabel, DTTitleLabel
from ui.dt_value_entry import DTValueEntry
from utils.dt_utils import DTUtils
from utils.dt_fonts import NonSerifNormal, NonSerifLight, NonSerifNormalSmall



class BarbarianSelectionDialog(DTBaseDialog):
    def __init__(self, parent=None):
        super().__init__("野蛮人", window_title="野蛮人")

        icon_path = DTUtils.resource_path('resources/icons/barbarian.jpeg')
        title_frame = ClassSelectionTitleFrame(
            parent=self,
            title="野蛮人 Barbarian",
            subtitle="具有原始狂怒的刚猛斗士",
            description="野蛮人是绝强的战士，他们与多元宇宙原力联结，以名为狂暴的方式展现力量。",
            icon_path=icon_path,
            primary_ability="力量",
            hp_die="D12",
            saves="力量，敏捷",
            skill_proficiency="选择两项：驯兽、运动、威吓、自然、察觉、求生",
            weapon_proficiency="简易和军用武器",
            armour_proficiency="轻甲、中甲和盾牌",
            starting_equipment1="巨斧，4把手斧，探索套组，15GP",
            starting_equipment2="75GP"
        )

        ability_frame = AbilityFrame(
            parent=self,
            cl="barbarian"
        )

        self.add_child('title', title_frame)
        self.add_child('ability', ability_frame)

        
class ClassSelectionTitleFrame(DTBaseFrame):
    def __init__(
            self,
            parent,
            title,
            subtitle,
            description,
            icon_path,
            primary_ability,
            hp_die,
            saves,
            skill_proficiency,
            weapon_proficiency,
            armour_proficiency,
            starting_equipment1,
            starting_equipment2,
    ):
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.icon_path = icon_path
        self.primary_ability = primary_ability
        self.hp_die = hp_die
        self.saves = saves
        self.skill_proficiency = skill_proficiency
        self.weapon_proficiency = weapon_proficiency
        self.armour_proficiency = armour_proficiency
        self.starting_equipment1 = starting_equipment1
        self.starting_equipment2 = starting_equipment2

        super().__init__(parent=parent)

    def _setup_content(self):
        self.title_frame = TitleFrame(self, self.title, self.subtitle, self.description, self.icon_path)

        self.pa_entry = DTValueEntry(
            label_text="主要属性",
            label_size=80,
            label_font=NonSerifNormal,
            editable=False,
            value_text=self.primary_ability,
            value_size=300,
            value_font=NonSerifLight,
            height=24
        )

        self.hp_entry = DTValueEntry(
            label_text="生命骰子",
            label_size=80,
            label_font=NonSerifNormal,
            editable=False,
            value_text=self.hp_die,
            value_size=300,
            value_font=NonSerifLight,
            height=24
        )

        self.saves_entry = DTValueEntry(
            label_text="豁免属性",
            label_size=80,
            label_font=NonSerifNormal,
            editable=False,
            value_text=self.saves,
            value_size=300,
            value_font=NonSerifLight,
            height=24
        )

        self.skill_entry = DTValueEntry(
            label_text="技能熟练",
            label_size=80,
            label_font=NonSerifNormal,
            editable=False,
            value_text=self.skill_proficiency,
            value_size=300,
            value_font=NonSerifLight,
            height=24
        )

        self.weapon_entry = DTValueEntry(
            label_text="武器精通",
            label_size=80,
            label_font=NonSerifNormal,
            editable=False,
            value_text=self.weapon_proficiency,
            value_size=300,
            value_font=NonSerifLight,
            height=24
        )

        self.armour_entry = DTValueEntry(
            label_text="护甲熟练",
            label_size=80,
            label_font=NonSerifNormal,
            editable=False,
            value_text=self.armour_proficiency,
            value_size=300,
            value_font=NonSerifLight,
            height=24
        )

        self.add_child('title', self.title_frame)
        self.add_component('primary_ability', self.pa_entry)
        self.add_component('hp_die', self.hp_entry)
        self.add_component('saves', self.saves_entry)
        self.add_component('weapon_proficiency', self.weapon_entry)
        self.add_component('armour_proficiency', self.armour_entry)


class TitleFrame(DTBaseFrame):
    def __init__(
            self,
            parent,
            title,
            subtitle,
            description,
            icon_path,
    ):
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.icon_path = icon_path

        super().__init__(parent=parent, layout_type=QHBoxLayout)

    def _setup_content(self):
        self.main_layout.setSpacing(20)

        self.text_frame = DTBaseFrame(self)

        title = DTTitleLabel(self.title, width=340)
        subtitle = DTSubLabel(self.subtitle, width=340)
        description = DTNormalLabel(self.description, width=340)

        self.text_frame.add_component('title', title)
        self.text_frame.add_component('subtitle', subtitle)
        self.text_frame.add_component('description', description)

        icon = QPixmap(self.icon_path)
        icon = icon.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.icon = QLabel(self)
        self.icon.setPixmap(icon)

        self.add_child('title', self.text_frame)
        self.add_component('icon_path', self.icon)


class AbilityFrame(DTBaseFrame):
    def __init__(
        self,
        parent,
        cl
    ):
        self.cl = cl

        super().__init__(parent=parent)

    def _setup_content(self):
        if self.cl == "barbarian":
            data = DTUtils.read_class_features('barbarian')

        for level, contents in data.items():
            for ability in contents:
                if ability['子职'] != '无':
                    continue
                ticket = DTExpandableTicket(
                    ability["中文名称"],
                    f"等级{level}",
                    self
                )
                ticket.scroll_area.main_layout.setSpacing(2)
                self.add_component('component', ticket)

                for line in ability["描述"]:
                    doc = QTextBrowser()
                    doc.setFrameStyle(0)
                    doc.setMarkdown(line.strip())
                    doc.setFont(NonSerifNormalSmall)
                    doc.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                    doc.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                    
                    doc.setSizePolicy(
                        QSizePolicy.Policy.Expanding,
                        QSizePolicy.Policy.Fixed
                    )
                    doc.document().documentLayout().documentSizeChanged.connect(
                        lambda _, d=doc: d.setFixedHeight(int(d.document().size().height()))
                    )
                    doc.setFixedHeight(int(doc.document().size().height()))

                    ticket.add_component(doc)
