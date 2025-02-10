from typing import List

from PyQt6.QtWidgets import QComboBox, QLabel, QLayout, QHBoxLayout, QCompleter
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ui.dt_base_frame import DTBaseFrame
from utils.dt_fonts import SerifLight, SerifNormal


class DTOptionEntry(DTBaseFrame):
    value_changed = pyqtSignal(str)
    validation_changed = pyqtSignal(bool)

    def __init__(
            self,
            label_text: str = "",
            label_size: int = 80,
            label_font: QFont = SerifNormal,
            label_alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            options: List[str] = [],
            options_size: int = 80,
            options_font: QFont = SerifLight,
            current_value: str = "",
            reverse: bool = False,
            height: int = 30,
            spacing: int = 30,
            enable: bool = True,
            filter: bool = False,
            layout: QLayout = QHBoxLayout,
            parent=None
    ):
        self.label_text = label_text
        self.label_size = label_size
        self.label_font = label_font
        self.label_alignment = label_alignment
        self.options = options
        self.options_size = options_size
        self.options_font = options_font
        self.current_value = current_value
        self.reverse = reverse
        self.height = height
        self.spacing = spacing
        self.enable = enable
        self.filter = filter

        self.completer = None
        
        super().__init__(layout_type=layout, parent=parent)
        
        self._is_valid = bool(self.current_value.strip())
        
        self.setFixedHeight(height)
        self.setFixedWidth(label_size + spacing + options_size)

    @property
    def is_valid(self):
        return self._is_valid

    def _setup_content(self):
        self.main_layout.setSpacing(self.spacing)

        self.label = QLabel(self.label_text)
        self.label.setFont(self.label_font)
        self.label.setFixedWidth(self.label_size)
        self.label.setFixedHeight(self.height)
        self.label.setAlignment(self.label_alignment)
        self.label.setStyleSheet("color: #000000;")

        self.combo = DTComboBox(self)
        self.combo.setFont(self.options_font)
        self.combo.setFixedWidth(max(self.options_size, 80))
        self.combo.setFixedHeight(self.height)
        self.combo.setEnabled(self.enable)

        self.combo.addItems(self.options)
        if self.current_value:
            index = self.combo.findText(self.current_value)
            if index >= 0:
                self.combo.setCurrentIndex(index)
            else:
                if self.filter:
                    self.combo.setEditText(self.current_value)
        else:
            if self.filter:
                self.combo.setEditText("")
            else:
                if self.combo.findText("") == -1:
                    self.combo.insertItem(0, "")
                self.combo.setCurrentIndex(0)

        self.combo.currentTextChanged.connect(self._on_option_selected)
        self.combo.currentTextChanged.connect(self._validate_selection)

        if self.filter:
            self._setup_filter()

        self.add_component('label', self.label)
        self.add_component('combo', self.combo)

    def _on_option_selected(self, value):
        self.value_changed.emit(value)

    def _validate_selection(self, value):
        new_valid = bool(value.strip())
        if new_valid != self._is_valid:
            self._is_valid = new_valid
            self.validation_changed.emit(new_valid)
        self.value_changed.emit(value)

    def _setup_filter(self):
        self.combo.setEditable(True)
        self.completer = QCompleter(self.options, self.combo)
        self.completer.setCompletionRole(Qt.ItemDataRole.DisplayRole)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.combo.setCompleter(self.completer)
        
        line_edit = self.combo.lineEdit()
        if line_edit:
            line_edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
            line_edit.setStyleSheet("QLineEdit { padding-left: 0px; matgin: 0px; }")

    def update_option(self, options):
        self.options = options
        self.combo.clear()
        self.combo.addItems(options)

        if self.filter and self.completer is not None:
            self.completer.model().setStringList(options)

    def get_value(self):
        return self.combo.currentText()
    
    def set_value(self, value):
        index = self.combo.findText(value)
        if index >= 0:
            self.combo.setCurrentIndex(index)
        else:
            if self.filter:
                self.combo.setEditText(value)

    def set_enabled(self, enable, all):
        self.combo.setEnabled(enable)
        if all:
            self.label.setEnabled(enable)


class DTComboBox(QComboBox):
    def showPopup(self):
        super().showPopup()
        popup = self.view().window()
        popup.move(popup.x(), popup.y() + 3)
