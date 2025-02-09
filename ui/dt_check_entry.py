from PyQt6.QtWidgets import QLayout, QHBoxLayout, QCheckBox, QWidget, QLabel
from PyQt6.QtCore import pyqtSignal, pyqtProperty, Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPainter, QColor

from ui.dt_base_frame import DTBaseFrame
from utils.dt_fonts import SerifNormal
from utils.dt_utils import DTUtils


class DTCheckEntry(DTBaseFrame):
    value_changed = pyqtSignal(bool)

    def __init__(
            self,
            label_text: str = "",
            label_size: int = 80,
            label_font: QFont = SerifNormal,
            label_alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            reverse: bool = False, 
            height: int = 30,
            spacing: int = 0,
            checked: bool = False,
            enable: bool = True,
            layout: QLayout = QHBoxLayout,
            parent=None
    ):
        self.label_text = label_text
        self.label_size = label_size
        self.label_font = label_font
        self.label_alignment = label_alignment
        self.reverse = reverse
        self.height = height
        self.spacing = spacing
        self.checked = checked
        self.enable = enable

        super().__init__(layout_type=layout, parent=parent)

        self.setFixedHeight(height)
        self.setFixedWidth(label_size + spacing + 15)

    def _setup_content(self):
        self.main_layout.setSpacing(self.spacing)

        self.label = QLabel(self.label_text)
        self.label.setFont(self.label_font)
        self.label.setFixedWidth(self.label_size)
        self.label.setFixedHeight(self.height)
        self.label.setAlignment(self.label_alignment)
        self.label.setStyleSheet("color: #000000;")

        self.check = DTCheckBox(self)
        self.set_checked(self.checked)
        self.check.stateChanged.connect(lambda state: self.value_changed.emit(bool(state)))

        self.set_enabled(self.enable)

        if self.reverse:
            self.add_component('label', self.label)
            self.add_component('checkbox', self.check)
        else:
            self.add_component('checkbox', self.check)
            self.add_component('label', self.label)

    def get_value(self):
        return self.check.isChecked()

    def _on_label_clicked(self, event) -> None:
        self.check.setChecked(not self.check.isChecked())

    def set_checked(self, checked):
        self.check.setChecked(checked)

    def set_enabled(self, enabled, all=False):
        self.check.setEnabled(enabled)
        if all:
            self.label.setEnabled(enabled)


class DTCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)

        self._overlay = HoverOverlay(self, corner_radius=4)
        self._overlay.setGeometry(self.rect())

        self._animation = QPropertyAnimation(self._overlay, b"opacity", self)
        self._animation.setDuration(100)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        icon_path = DTUtils.resource_path('resources/icons/check.png').replace('\\', '/')
        self.setStyleSheet(f"""
            QCheckBox {{
                background-color: white;
                border-radius: 6px;
                padding: 3px;
            }}
            
            QCheckBox::indicator {{
                width: 15px;
                height: 15px;
                border-radius: 4px;
                border: 2px solid #666666;
                background: white;
            }}
            
            QCheckBox::indicator:checked {{
                image: url("{icon_path}");
                border: 2px solid #388E3C;
                border-radius: 4px;
            }}
            
            QCheckBox::indicator:hover {{
                border: 2px solid #888888;
            }}
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._overlay.setGeometry(self.rect())

    def enterEvent(self, event):
        if not self.isEnabled():
            return super().enterEvent(event)
        self._animation.stop()
        self._animation.setStartValue(self._overlay.opacity)
        self._animation.setEndValue(0.15)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self._overlay.opacity)
        self._animation.setEndValue(0.0)
        self._animation.start()
        super().leaveEvent(event)

    def setEnabled(self, enabled: bool) -> None:
        super().setEnabled(enabled)
        if not enabled:
            self._animation.stop()
            self._overlay.setOpacity(0.0)


class HoverOverlay(QWidget):
    def __init__(self, parent=None, corner_radius: int = 4):
        super().__init__(parent)
        self._opacity = 0.0
        self._corner_radius = corner_radius
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent;")
        self.setAutoFillBackground(False)

    def getOpacity(self) -> float:
        return self._opacity

    def setOpacity(self, value: float) -> None:
        self._opacity = value
        self.update()

    opacity = pyqtProperty(float, fget=getOpacity, fset=setOpacity)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        alpha = int(self._opacity * 255)
        painter.setBrush(QColor(255, 255, 255, alpha))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self._corner_radius, self._corner_radius)
        painter.end()
