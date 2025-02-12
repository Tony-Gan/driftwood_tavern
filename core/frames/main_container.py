from PyQt6.QtWidgets import QDialog

from core.dialogs.class_selection import BarbarianSelectionDialog
from ui.dt_base_button import DTClassButton
from ui.dt_base_frame import DTBaseFrame
from ui.dt_check_entry import DTCheckEntry
from ui.dt_label import DTSubLabel, DTTitleLabel
from ui.dt_stack_widget import DTStackedWidget
from utils.dt_fonts import NonSerifNormal
from utils.dt_utils import DTUtils


class MainContainer(DTBaseFrame):
    def __init__(self, parent, p_data):
        self.p_data = p_data
        super().__init__(parent=parent)

    def _setup_content(self):
        self.setFixedHeight(830)

        self.stack = DTStackedWidget(self)

        self.settings_frame = SettingsFrame(self)
        self.class_frame = ClassFrame(self)
        
        self.stack.addWidget(self.settings_frame)
        self.stack.addWidget(self.class_frame)

        self.stack.setCurrentWidget(self.settings_frame)
        self.main_layout.addWidget(self.stack)

    def switch_to_settings(self):
        self.stack.setCurrentWidget(self.settings_frame)

    def switch_to_previous(self):
        current_index = self.stack.currentIndex()
        if current_index > 0:
            self.stack.setCurrentIndex(current_index - 1)
        else:
            pass

    def switch_to_next(self):
        current_index = self.stack.currentIndex()
        if current_index < self.stack.count() - 1:
            self.stack.setCurrentIndex(current_index + 1)
        else:
            pass

    def register_cl(self, cl):
        self.p_data.cl = cl


class SettingsFrame(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def _setup_content(self):
        self.label1 = DTTitleLabel(text="基础规则", parent=self)
        self.text1 = DTSubLabel(
            text="所使用的基础规则，不同版本的基础规则将带来差别很大的构筑体验，如果你不知道你要选择哪个，那么请咨询你的KP，或者选择2014版本", 
            width=600,
            parent=self
        )

        self.pbh2014 = DTCheckEntry(
            label_text='玩家手册2014',
            label_size=120,
            label_font=NonSerifNormal
        )
        self.pbh2014.value_changed.connect(self._on_pbh2014_changed)

        self.pbh2024 = DTCheckEntry(
            label_text='玩家手册2024',
            label_size=120,
            label_font=NonSerifNormal
        )
        self.pbh2024.value_changed.connect(self._on_pbh2024_changed)

        self.label2 = DTTitleLabel(text="扩展规则", parent=self)
        self.text2 = DTSubLabel(
            text="所使用的扩展规则，这些扩展增加了新的职业，子职，法术，物品等；与你的KP交流可以使用的扩展，如果你是D&D新手，建议不要启用扩展", 
            width=600,
            parent=self
        )

        self.scag = DTCheckEntry(
            label_text='剑湾书扩展',
            label_size=120,
            label_font=NonSerifNormal
        )

        self.xge = DTCheckEntry(
            label_text='眼魔书扩展',
            label_size=120,
            label_font=NonSerifNormal
        )

        self.tce = DTCheckEntry(
            label_text='塔莎书扩展',
            label_size=120,
            label_font=NonSerifNormal
        )

        self.add_component('title1', self.label1)
        self.add_component('text1', self.text1)
        self.add_component('phb2014', self.pbh2014)
        self.add_component('phb2024', self.pbh2024)
        self.add_component('title2', self.label2)
        self.add_component('text1', self.text2)
        self.add_component('scag', self.scag)
        self.add_component('xge', self.xge)
        self.add_component('tce', self.tce)

        self.main_layout.addStretch()

    def _on_pbh2014_changed(self, checked):
        if checked:
            self.pbh2024.set_checked(False)

    def _on_pbh2024_changed(self, checked):
        if checked:
            self.pbh2014.set_checked(False)


class ClassFrame(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def _setup_content(self):
        self.label1 = DTTitleLabel(text="选择你的职业", width=600, parent=self)
        
        self.class1 = DTClassButton(
            text='野蛮人',
            icon_path=DTUtils.resource_path("resources/icons/barbarian.jpeg"),
            parent=self
        )

        self.class2 = DTClassButton(
            text='吟游诗人',
            icon_path=DTUtils.resource_path("resources/icons/bard.jpeg"),
            parent=self
        )

        self.class3 = DTClassButton(
            text='牧师',
            icon_path=DTUtils.resource_path("resources/icons/cleric.jpeg"),
            parent=self
        )

        self.class4 = DTClassButton(
            text='德鲁伊',
            icon_path=DTUtils.resource_path("resources/icons/druid.jpeg"),
            parent=self
        )

        self.class5 = DTClassButton(
            text='战士',
            icon_path=DTUtils.resource_path("resources/icons/fighter.jpeg"),
            parent=self
        )

        self.class6 = DTClassButton(
            text='武僧',
            icon_path=DTUtils.resource_path("resources/icons/monk.jpeg"),
            parent=self
        )

        self.class7 = DTClassButton(
            text='圣骑士',
            icon_path=DTUtils.resource_path("resources/icons/paladin.jpeg"),
            parent=self
        )

        self.class8 = DTClassButton(
            text='游侠',
            icon_path=DTUtils.resource_path("resources/icons/ranger.jpeg"),
            parent=self
        )

        self.class9 = DTClassButton(
            text='游荡者',
            icon_path=DTUtils.resource_path("resources/icons/rogue.jpeg"),
            parent=self
        )

        self.class10 = DTClassButton(
            text='术士',
            icon_path=DTUtils.resource_path("resources/icons/sorcerer.jpeg"),
            parent=self
        )

        self.class11 = DTClassButton(
            text='魔契师',
            icon_path=DTUtils.resource_path("resources/icons/warlock.jpeg"),
            parent=self
        )

        self.class12 = DTClassButton(
            text='法师',
            icon_path=DTUtils.resource_path("resources/icons/wizard.jpeg"),
            parent=self
        )

        self.add_component('title1', self.label1)
        self.add_component('barbarian', self.class1)
        self.add_component('bard', self.class2)
        self.add_component('cleric', self.class3)
        self.add_component('druid', self.class4)
        self.add_component('fighter', self.class5)
        self.add_component('monk', self.class6)
        self.add_component('paladin', self.class7)
        self.add_component('ranger', self.class8)
        self.add_component('rogue', self.class9)
        self.add_component('sorcerer', self.class10)
        self.add_component('warlock', self.class11)
        self.add_component('wizard', self.class12)

        self.class1.clicked.connect(self._on_barbarian_clicked)
        self.class2.clicked.connect(self._on_bard_clicked)
        self.class3.clicked.connect(self._on_cleric_clicked)
        self.class4.clicked.connect(self._on_druid_clicked)
        self.class5.clicked.connect(self._on_fighter_clicked)
        self.class6.clicked.connect(self._on_monk_clicked)
        self.class7.clicked.connect(self._on_paladin_clicked)
        self.class8.clicked.connect(self._on_ranger_clicked)
        self.class9.clicked.connect(self._on_rogue_clicked)
        self.class10.clicked.connect(self._on_sorcerer_clicked)
        self.class11.clicked.connect(self._on_warlock_clicked)
        self.class12.clicked.connect(self._on_wizard_clicked)

        self.main_layout.addStretch()

    def _on_barbarian_clicked(self):
        success, results = BarbarianSelectionDialog.get_input(self)
        if not success:
            return
        print(results)

    def _on_bard_clicked(self):
        print(1)

    def _on_cleric_clicked(self):
        print(1)

    def _on_druid_clicked(self):
        print(1)

    def _on_fighter_clicked(self):
        print(1)

    def _on_monk_clicked(self):
        print(1)

    def _on_paladin_clicked(self):
        print(1)

    def _on_ranger_clicked(self):
        print(1)

    def _on_rogue_clicked(self):
        print(1)

    def _on_sorcerer_clicked(self):
        print(1)

    def _on_warlock_clicked(self):
        print(1)

    def _on_wizard_clicked(self):
        print(1)
