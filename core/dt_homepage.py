from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

from ui.dt_base_button import DTStandardButton, DTWarningButton
from ui.dt_base_frame import DTBaseFrame
from utils.dt_utils import DTUtils


class DTHomePage(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def _setup_content(self):
        logo_label = QLabel()
        logo_pixmap = QPixmap(DTUtils.resource_path('resources/icons/app.png'))
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.add_component('logo', logo_label)

        buttons_frame = ButtonsFrame(self)
        self.add_child('buttons', buttons_frame)


class ButtonsFrame(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def _setup_content(self):
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setContentsMargins(0, 100, 0, 100)
        self.main_layout.setSpacing(25)

        font = QFont("Noto Sans SC SemiBold")
        font.setPointSize(16)

        button1 = DTStandardButton(
            f'创建角色', 
            icon_path=DTUtils.resource_path('resources/icons/app.png'),
            width=300,
            height=80,
            radius=10,
            font=font,
            parent=self
        )
        self.add_component('btn1', button1)
        button1.clicked.connect(self.goto_create_character)

        button2 = DTStandardButton(
            f'管理角色', 
            icon_path=DTUtils.resource_path('resources/icons/app.png'),
            width=300,
            height=80,
            radius=10,
            font=font,
            parent=self
        )
        self.add_component('btn2', button2)
        button2.clicked.connect(self.goto_manage_character)

        button3 = DTWarningButton(
            f'离开酒馆', 
            icon_path=DTUtils.resource_path('resources/icons/app.png'),
            width=300,
            height=80,
            radius=10,
            font=font,
            parent=self
        )
        self.add_component('btn3', button3)
        button3.clicked.connect(self.leave_tavern)

    def goto_create_character(self):
        self.parent.parent.switch_to_create_character()

    def goto_manage_character(self):
        self.parent.parent.switch_to_manage_character()

    def leave_tavern(self):
        self.parent.parent.close()
