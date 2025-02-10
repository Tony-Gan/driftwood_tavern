from PyQt6.QtWidgets import QHBoxLayout, QStackedLayout, QButtonGroup, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from core.dialogs.class_selection import BarbarianSelectionDialog
from ui.dt_base_button import DTClassButton, DTToggleButton
from ui.dt_base_frame import DTBaseFrame
from ui.dt_check_entry import DTCheckEntry
from ui.dt_label import DTSubLabel, DTTitleLabel
from ui.dt_stack_widget import DTStackedWidget
from ui.dt_value_entry import DTValueEntry
from utils.dt_fonts import TitleChinese, NonSerifNormal, NonSerifLight
from utils.dt_utils import DTUtils


class DTCharacterBuilder(DTBaseFrame):
    def __init__(self, parent):
        self.p_data = {}
        super().__init__(parent=parent)

    def _setup_content(self):
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.progress_bar = ProgressBar(self)
        self.basic_info_bar = BasicInfoBar(self)
        self.main_container = MainContainer(self)

        self.add_child('progress_bar', self.progress_bar)
        self.add_child('basic_info_bar', self.basic_info_bar)
        self.add_child('main_container', self.main_container)

class ProgressBar(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(layout_type=QHBoxLayout, parent=parent)

    def _setup_content(self):
        self.setFixedHeight(80)
        texts = ["基础设置", "职业设置", "角色背景", "种族设置", "能力设置", "装备设置", "完成"]

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for t in texts:
            btn = DTToggleButton(text=t, height=48, width=100, font=TitleChinese, parent=self)
            self.add_component(t, btn)
            self.button_group.addButton(btn)
            if t == "基础设置":
                btn.setChecked(True)

        self.button_group.buttonClicked.connect(self.on_button_clicked)

        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(20)

    def on_button_clicked(self, clicked_button):
        if clicked_button.text() == "基础设置":
            self.parent.main_container.stack.setCurrentWidget(self.parent.main_container.settings_frame)
        if clicked_button.text() == "职业设置":
            self.parent.main_container.stack.setCurrentWidget(self.parent.main_container.class_frame)


class BasicInfoBar(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(layout_type=QHBoxLayout, parent=parent)

    def _setup_content(self):
        self.setFixedHeight(80)
        self.main_layout.setSpacing(40)

        self.avatar_frame = AvatarFrame(self)
        self.info_frame = InfoFrame(self)

        pixmap_previous = QPixmap(DTUtils.resource_path("resources/icons/previous.png"))
        pixmap_previous = pixmap_previous.scaled(50, 50, 
                                      Qt.AspectRatioMode.KeepAspectRatio, 
                                      Qt.TransformationMode.SmoothTransformation)
        
        pixmap_next = QPixmap(DTUtils.resource_path("resources/icons/next.png"))
        pixmap_next = pixmap_next.scaled(50, 50, 
                                      Qt.AspectRatioMode.KeepAspectRatio, 
                                      Qt.TransformationMode.SmoothTransformation)
        
        self.previous = QLabel(self)
        self.previous.setPixmap(pixmap_previous)
        self.previous.mousePressEvent = self._on_previous_clicked

        self.next = QLabel(self)
        self.next.setPixmap(pixmap_next)
        self.next.mousePressEvent = self._on_next_clicked
        
        self.main_layout.addStretch()
        self.main_layout.addStretch()
        self.add_component('previous', self.previous)
        self.main_layout.addStretch()
        self.add_child('avatar_frame', self.avatar_frame)
        self.add_child('info_frame', self.info_frame)
        self.main_layout.addStretch()
        self.add_component('next', self.next)
        self.main_layout.addStretch()
        self.main_layout.addStretch()

    def _on_previous_clicked(self, event):
        self.parent.main_container.switch_to_previous()

    def _on_next_clicked(self, event):
        self.parent.main_container.switch_to_next()


class AvatarFrame(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(layout_type=QStackedLayout, parent=parent)

    def _setup_content(self):
        self.setFixedSize(60, 60)
        self.setStyleSheet("""
            QFrame {
                border: 1px dashed black;
            }
        """)

        self.silhouette_label = QLabel(self)
        pixmap_sil = QPixmap(DTUtils.resource_path("resources/icons/default_avatar.png"))
        pixmap_sil = pixmap_sil.scaled(self.width() - 10, self.height() - 10, 
                                      Qt.AspectRatioMode.KeepAspectRatio, 
                                      Qt.TransformationMode.SmoothTransformation)
        self.silhouette_label.setPixmap(pixmap_sil)
        self.silhouette_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_component('silhouette_label', self.silhouette_label)

        self.plus_label = QLabel(self)
        pixmap_plus = QPixmap(DTUtils.resource_path("resources/icons/upload.png"))
        pixmap_plus = pixmap_plus.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.TransformationMode.SmoothTransformation)
        self.plus_label.setPixmap(pixmap_plus)
        self.plus_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_component('plus_label', self.plus_label)

        self.main_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)


class InfoFrame(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def _setup_content(self):
        self.setFixedHeight(70)
        self.setFixedWidth(140)
        self.char_name = DTValueEntry(
            label_text='角色名',
            label_size=50,
            label_font=NonSerifNormal,
            value_size=80,
            value_font=NonSerifLight
        )

        self.pl_name = DTValueEntry(
            label_text='玩家名',
            label_size=50,
            label_font=NonSerifNormal,
            value_size=80,
            value_font=NonSerifLight
        )

        self.add_component('char_name', self.char_name)
        self.add_component('pl_name', self.pl_name)


class MainContainer(DTBaseFrame):
    def __init__(self, parent):
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
        dialog = BarbarianSelectionDialog(self)
        dialog.exec()

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
