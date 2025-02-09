import math

from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QGraphicsColorizeEffect
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

from utils.dt_utils import DTUtils
from utils.dt_fonts import SerifLight, SerifMediumLarge


class DTBaseButton(QPushButton):
    def __init__(self, 
                 text: str = "", 
                 icon_path: str = None,
                 width: int = 80, 
                 height: int = 24, 
                 font: QFont = None, 
                 parent=None):
        super().__init__(parent)

        self.setFixedWidth(width)
        self.setFixedHeight(height)

        margin = math.ceil(width / 8)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(margin, 0, margin, 0)
        layout.setSpacing(margin)

        self.label_text = QLabel(text)
        if font is not None:
            self.label_text.setFont(font)
        else:
            self.label_text.setFont(SerifLight)

        if not icon_path:
            self.label_icon = None
            layout.addWidget(self.label_text, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            self.label_icon = QLabel(self)
            pixmap = QPixmap(icon_path)
            pixmap = pixmap.scaled(math.floor(height * 0.6), math.floor(height * 0.6),
                                   Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)
            self.label_icon.setPixmap(pixmap)

            layout.addWidget(self.label_text, alignment=Qt.AlignmentFlag.AlignLeft)
            
            layout.addWidget(self.label_icon, alignment=Qt.AlignmentFlag.AlignRight)

        self.hover_effect = QGraphicsColorizeEffect(self)
        self.hover_effect.setColor(QColor("white"))
        self.hover_effect.setStrength(0.0)
        self.setGraphicsEffect(self.hover_effect)

        self._enter_animation = QPropertyAnimation(self.hover_effect, b"strength", self)
        self._enter_animation.setDuration(150)
        self._enter_animation.setStartValue(0.0)
        self._enter_animation.setEndValue(0.25)
        self._enter_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._leave_animation = QPropertyAnimation(self.hover_effect, b"strength", self)
        self._leave_animation.setDuration(150)
        self._leave_animation.setStartValue(0.25)
        self._leave_animation.setEndValue(0.0)
        self._leave_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event):
        self._leave_animation.stop()
        self._enter_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._enter_animation.stop()
        self._leave_animation.start()
        super().leaveEvent(event)

    def text(self):
        return self.label_text.text()

class DTWarningButton(DTBaseButton):
    def __init__(self,
                 text: str = "",
                 icon_path: str = None,
                 width: int = 80,
                 height: int = 24,
                 font: QFont = None,
                 radius: int = 3,
                 parent=None):
        super().__init__(text, icon_path, width, height, font, parent)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #E40712;
                border: none;
                border-radius: {radius}px;
            }}
        """)

        self.label_text.setStyleSheet("color: #FFFFFF;")


class DTStandardButton(DTBaseButton):
    def __init__(self,
                 text: str = "",
                 icon_path: str = None,
                 width: int = 80,
                 height: int = 24,
                 font: QFont = None,
                 radius: int = 3,
                 parent=None):
        super().__init__(text, icon_path, width, height, font, parent)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #232B2F;
                border: none;
                border-radius: {radius}px;
            }}
        """)

        self.label_text.setStyleSheet("color: #FFFFFF;")


class DTToggleButton(DTBaseButton):
    def __init__(
        self,
        text: str = "",
        icon_path: str = None,
        width: int = 80,
        height: int = 24,
        font: QFont = None,
        radius: int = 3,
        parent=None
    ):
        super().__init__(text, icon_path, width, height, font, parent)

        self.setCheckable(True)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: none;
                border: none;
                border-radius: {radius}px;
            }}
            QPushButton:checked {{
                background-color: #C0C0C0;
            }}
        """)

        self.label_text.setStyleSheet("color: #000000;")


class DTClassButton(QPushButton):
    def __init__(self, 
                 text: str = "", 
                 icon_path: str = None,
                 parent=None):
        super().__init__(parent)

        self.setFixedWidth(600)
        self.setFixedHeight(50)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        self.label_text = QLabel(text, self)
        self.label_text.setFont(SerifMediumLarge)

        self.icon1 = QLabel(self)
        pixmap1 = QPixmap(icon_path)
        pixmap1 = pixmap1.scaled(30, 30,
                                Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation)
        self.icon1.setPixmap(pixmap1)

        self.icon2 = QLabel(self)
        pixmap2 = QPixmap(DTUtils.resource_path("resources/icons/next.png"))
        pixmap2 = pixmap2.scaled(30, 30,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation)
        self.icon2.setPixmap(pixmap2)

        layout.addWidget(self.icon1)
        layout.addWidget(self.label_text)
        layout.addStretch()
        layout.addWidget(self.icon2)

        self.hover_effect = QGraphicsColorizeEffect(self)
        self.hover_effect.setColor(QColor("white"))
        self.hover_effect.setStrength(0.0)
        self.setGraphicsEffect(self.hover_effect)

        self._enter_animation = QPropertyAnimation(self.hover_effect, b"strength", self)
        self._enter_animation.setDuration(150)
        self._enter_animation.setStartValue(0.0)
        self._enter_animation.setEndValue(0.25)
        self._enter_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._leave_animation = QPropertyAnimation(self.hover_effect, b"strength", self)
        self._leave_animation.setDuration(150)
        self._leave_animation.setStartValue(0.25)
        self._leave_animation.setEndValue(0.0)
        self._leave_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #FFFFFF;
                border: 1px solid #555555;
                border-radius: 5px;
            }}
        """)

        self.label_text.setStyleSheet("color: #000000;")

    def enterEvent(self, event):
        self._leave_animation.stop()
        self._enter_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._enter_animation.stop()
        self._leave_animation.start()
        super().leaveEvent(event)

    def text(self):
        return self.label_text.text()
