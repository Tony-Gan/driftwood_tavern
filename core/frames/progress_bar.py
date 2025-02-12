from PyQt6.QtWidgets import QHBoxLayout, QButtonGroup
from PyQt6.QtCore import Qt

from ui.dt_base_button import DTToggleButton
from ui.dt_base_frame import DTBaseFrame
from utils.dt_fonts import TitleChinese

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
