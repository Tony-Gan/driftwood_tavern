from PyQt6.QtWidgets import QLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from ui.dt_base_frame import DTBaseFrame
from ui.dt_line_edit import DTLineEdit
from utils.dt_fonts import SerifLight, SerifNormal


class DTValueEntry(DTBaseFrame):
    value_changed = pyqtSignal(str)

    def __init__(
            self,
            label_text: str = "",
            label_size: int = 80,
            label_font: QFont = SerifNormal,
            label_alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            value_text: str = "",
            value_size: int = 80,
            value_font: QFont = SerifLight,
            value_alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            height: int = 30,
            spacing: int = 0,
            enable: bool = True,
            layout: QLayout = QHBoxLayout,
            parent=None
    ):
        self.label_text = label_text
        self.label_size = label_size
        self.label_font = label_font
        self.label_alignment = label_alignment
        self.value_text = value_text
        self.value_size = value_size
        self.value_font = value_font
        self.value_aligment = value_alignment
        self.height = height
        self.spacing = spacing
        self.enable = enable

        super().__init__(layout_type=layout, parent=parent)

        self.setFixedHeight(height)
        self.setFixedWidth(label_size + spacing + value_size)

    def _setup_content(self):
        self.main_layout.setSpacing(self.spacing)

        self.label = QLabel(self.label_text)
        self.label.setFont(self.label_font)
        self.label.setFixedWidth(self.label_size)
        self.label.setFixedHeight(self.height)
        self.label.setAlignment(self.label_alignment)
        self.label.setStyleSheet("color: #000000;")

        self.entry = DTLineEdit(
            self.value_size,
            self.height,
            self.value_font,
            self.value_aligment,
            self
        )

        self.set_enable(self.enable)

        self.add_component('label', self.label)
        self.add_component('entry', self.entry)

    def get_value(self):
        return self.entry.text()

    def set_value(self, value: str):
        self.entry.setText(str(value))

    def set_enable(self, enabled, all=False):
        self.entry.setEnabled(enabled)
        if all:
            self.label.setEnabled(enabled)
