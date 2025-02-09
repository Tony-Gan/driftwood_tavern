from PyQt6.QtWidgets import QLineEdit, QGraphicsDropShadowEffect
from PyQt6.QtCore import pyqtProperty, QPropertyAnimation, QEasingCurve, Qt
from PyQt6.QtGui import QColor, QCursor, QFont

class DTLineEdit(QLineEdit):
    def __init__(
            self,
            width: int = 80,
            height: int = 30,
            font: QFont = None,
            alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            parent = None
    ):
        super().__init__(parent)

        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setFont(font if font else SerifLight)
        self.setAlignment(alignment)

        self._default_color = QColor("#C0C0C0")
        self._hover_color   = QColor("#AAAAAA")
        self._focus_color   = QColor("#000000")

        self._default_shadow = 0
        self._focus_shadow = 3

        self._border_color = self._default_color
        self._shadow_blur  = self._default_shadow

        self._shadow_effect = QGraphicsDropShadowEffect(self)
        self._shadow_effect.setColor(QColor(0, 0, 0, 120))
        self._shadow_effect.setOffset(0, 2)
        self._shadow_effect.setBlurRadius(self._shadow_blur)
        self.setGraphicsEffect(self._shadow_effect)

        self._color_anim = QPropertyAnimation(self, b"border_color", self)
        self._color_anim.setDuration(200)
        self._color_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._shadow_anim = QPropertyAnimation(self, b"shadow_blur", self)
        self._shadow_anim.setDuration(200)
        self._shadow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.updateStyleSheet()

    @pyqtProperty(QColor)
    def border_color(self) -> QColor:
        return self._border_color

    @border_color.setter
    def border_color(self, new_color: QColor):
        self._border_color = new_color
        self.updateStyleSheet()

    def updateStyleSheet(self):
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {self._border_color.name()};
                border-radius: 5px;
                background: #FFFFFF;
                padding: 3px;
                color: black;
            }}
        """)

    @pyqtProperty(float)
    def shadow_blur(self) -> float:
        return self._shadow_blur

    @shadow_blur.setter
    def shadow_blur(self, val: float):
        self._shadow_blur = val
        self._shadow_effect.setBlurRadius(val)

    def enterEvent(self, event):
        if not self.hasFocus():
            self._color_anim.stop()
            self._color_anim.setStartValue(self.border_color)
            self._color_anim.setEndValue(self._hover_color)
            self._color_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.hasFocus():
            self._color_anim.stop()
            self._color_anim.setStartValue(self.border_color)
            self._color_anim.setEndValue(self._default_color)
            self._color_anim.start()
        super().leaveEvent(event)

    def focusInEvent(self, event):
        self._color_anim.stop()
        self._color_anim.setStartValue(self.border_color)
        self._color_anim.setEndValue(self._focus_color)
        self._color_anim.start()

        self._shadow_anim.stop()
        self._shadow_anim.setStartValue(self.shadow_blur)
        self._shadow_anim.setEndValue(self._focus_shadow)
        self._shadow_anim.start()

        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self._shadow_anim.stop()
        self._shadow_anim.setStartValue(self.shadow_blur)
        self._shadow_anim.setEndValue(self._default_shadow)
        self._shadow_anim.start()

        under_mouse = self.rect().contains(self.mapFromGlobal(QCursor.pos()))
        end_color = self._hover_color if under_mouse else self._default_color

        self._color_anim.stop()
        self._color_anim.setStartValue(self.border_color)
        self._color_anim.setEndValue(end_color)
        self._color_anim.start()

        super().focusOutEvent(event)
    