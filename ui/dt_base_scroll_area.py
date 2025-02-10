from typing import Any
from PyQt6.QtWidgets import QFrame, QScrollArea, QVBoxLayout, QLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt

from ui.dt_option_entry import DTOptionEntry
from ui.interfaces.idt_container import IDTContainer


class DTBaseScrollArea(QScrollArea, IDTContainer):
    values_changed = pyqtSignal(dict)
    content_height_changed = pyqtSignal(int)
    all_valid = pyqtSignal(bool)

    def __init__(
            self, 
            parent, 
            layout_type: type[QLayout] = QVBoxLayout, 
            alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
            auto_adjust_height: bool = False
    ):
        super().__init__(parent)

        self.parent = parent
        self.container = QFrame()
        self.container.setFrameShape(QFrame.Shape.NoFrame)
        self.main_layout = layout_type(self.container)
        self.main_layout.setAlignment(alignment)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.container.setLayout(self.main_layout)
        self._value_entries = {}

        self.setWidget(self.container)
        self.setWidgetResizable(True)

        self.auto_adjust_enabled = auto_adjust_height
        self._content_height = 0

        if self.auto_adjust_enabled:
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        else:
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if not issubclass(layout_type, QLayout):
            raise TypeError(f"Invalid layout_type: {layout_type}. Expected a subclass of QLayout.")

        self.init_interface()

        self.setFrameShape(QFrame.Shape.NoFrame)
        
        self._setup_content()

        if self.auto_adjust_enabled:
            self.main_layout.layoutChanged.connect(self._update_content_height)

    def _setup_content(self) -> None:
        pass

    def showEvent(self, event):
        if self.auto_adjust_enabled:
            super().showEvent(event)
            self._update_content_height()

    def set_auto_adjust(self, enable: bool):
        self.auto_adjust_enabled = enable
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding if enable 
            else QSizePolicy.Policy.Expanding
        )
        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff if enable
            else Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

    def _update_content_height(self):
        if not self.auto_adjust_enabled:
            return
            
        new_height = self.container.sizeHint().height()
        if new_height != self._content_height:
            self._content_height = new_height
            self.content_height_changed.emit(new_height)
            self.updateGeometry()

    def add_child(self, name: str, child: "IDTContainer", alignment: Qt.AlignmentFlag = None):
        super().add_child(name, child, alignment)
        self._track_validation(name, child)

    def add_component(self, name: str, component: Any):
        super().add_component(name, component)
        self._track_validation(name, component)

    def _track_validation(self, name: str, component: Any):
        if isinstance(component, DTOptionEntry):
            component.validation_changed.connect(
                lambda valid: self._update_validation(name, valid)
            )
            self._value_entries[name] = component.is_valid
            self._check_all_valid()

    def _update_validation(self, name: str, valid: bool):
        self._value_entries[name] = valid
        self._check_all_valid()

    def _check_all_valid(self):
        if not self._value_entries:
            self.all_valid.emit(True)
            return
            
        all_valid = all(self._value_entries.values())
        self.all_valid.emit(all_valid)

    def sizeHint(self):
        if self.auto_adjust_enabled:
            hint = super().sizeHint()
            hint.setHeight(self._content_height + self.frameWidth() * 2)
            return hint
        return super().sizeHint()

    