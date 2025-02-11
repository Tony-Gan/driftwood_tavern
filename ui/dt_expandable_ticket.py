from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QGraphicsColorizeEffect
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QPixmap, QColor

from ui.dt_base_frame import DTBaseFrame
from ui.dt_base_scroll_area import DTBaseScrollArea
from utils.dt_utils import DTUtils
from utils.dt_fonts import NonSerifNormal, NonSerifLightSub

class DTExpandableTicket(QWidget):
    expanded_changed = pyqtSignal(bool)

    def __init__(self, text: str = "", sub_text: str = "", parent=None):
        super().__init__(parent)
        self.is_expanded = False
        self.expand_icon = DTUtils.resource_path("resources/icons/expand.png")
        self.collapse_icon = DTUtils.resource_path("resources/icons/collapse.png")
        self._max_height = 800
        self._min_height = 100

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.header = QPushButton()
        self.header.setFixedHeight(50)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._setup_header(text, sub_text)
        
        self.scroll_area = DTBaseScrollArea(
            self,
            auto_adjust_height=True,
            alignment=Qt.AlignmentFlag.AlignTop
        )
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setMinimumHeight(0)
        self.scroll_area.setMaximumHeight(0)
        
        self.scroll_area.content_height_changed.connect(self._adjust_scroll_height)
        
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.scroll_area)
        
        self._setup_style()
        self._setup_validation_style()
        self.scroll_area.all_valid.connect(self._update_validation_style)

        QTimer.singleShot(0, self._initial_validate)

    def _setup_header(self, text: str, sub_text: str):
        layout = QHBoxLayout(self.header)
        layout.setContentsMargins(20, 5, 20, 5)
        layout.setSpacing(15)

        
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.text_label.setFont(NonSerifNormal)

        self.sub_text_label = QLabel(sub_text)
        self.sub_text_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.sub_text_label.setFont(NonSerifLightSub)

        self.entry = DTBaseFrame(parent=self)
        self.entry.setStyleSheet("background-color: transparent;")
        self.entry.add_component('title', self.text_label)
        self.entry.add_component('sub_text', self.sub_text_label)
        
        self.state_icon = QLabel()
        self._update_icon()
        
        layout.addWidget(self.entry)
        layout.addStretch()
        layout.addWidget(self.state_icon)
        
        self.header.clicked.connect(self.toggle_expansion)
        self._setup_hover_effect()

    def _setup_hover_effect(self):
        self.hover_effect = QGraphicsColorizeEffect(self.header)
        self.hover_effect.setColor(QColor("#E0E0E0"))
        self.hover_effect.setStrength(0.0)
        self.header.setGraphicsEffect(self.hover_effect)

        self.enter_anim = QPropertyAnimation(self.hover_effect, b"strength")
        self.enter_anim.setDuration(150)
        self.enter_anim.setStartValue(0.0)
        self.enter_anim.setEndValue(0.4)
        self.enter_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.leave_anim = QPropertyAnimation(self.hover_effect, b"strength")
        self.leave_anim.setDuration(150)
        self.leave_anim.setStartValue(0.4)
        self.leave_anim.setEndValue(0.0)
        self.leave_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _setup_style(self):
        self.header.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                border: none;
            }
        """)
        self.text_label.setStyleSheet("""
            QLabel {
                font-size: 14px; 
                color: #333333;
                background-color: #F0F0F0;
            }
        """)
        self.sub_text_label.setStyleSheet("""
            QLabel {
                font-size: 12px; 
                color: #666666;
                background-color: #F0F0F0;
            }
        """)
        self.state_icon.setStyleSheet("background-color: transparent;")

    def _setup_validation_style(self):
        self._valid_style = """
            QPushButton {
                background-color: #F0F0F0;
                border: none;
            }
        """
        self._invalid_style = """
            QPushButton {
                background-color: #F0F0F0;
                border-top: 1px solid #FF5252;
                border-right: none;
                border-left: none;
                border-bottom: none;
            }
        """
        self._normal_style = self.header.styleSheet()

    def _initial_validate(self):
        is_valid = self._get_option_entries_validity()
        self._update_validation_style(is_valid)

    def _get_option_entries_validity(self):
        valid = True
        layout = self.scroll_area.widget().layout()
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget is not None and hasattr(widget, 'is_valid'):
                if not widget.is_valid:
                    valid = False
                    break
        return valid

    def _update_validation_style(self, is_valid: bool):
        if is_valid:
            self.header.setStyleSheet(self._valid_style)
        else:
            self.header.setStyleSheet(self._invalid_style)

    def _adjust_scroll_height(self, content_height: int):
        if self.is_expanded:
            clamped_height = max(self._min_height, min(content_height, self._max_height))
        else:
            clamped_height = 0
        self.scroll_area.setMaximumHeight(clamped_height)
        self.updateGeometry()

    def toggle_expansion(self):
        self.is_expanded = not self.is_expanded
        self._update_validation_style(self._get_option_entries_validity())
        self._update_icon()
        self._animate_expansion()
        self.expanded_changed.emit(self.is_expanded)

    def _animate_expansion(self):
        if self.is_expanded:
            content_height = self.scroll_area.widget().sizeHint().height()
            target_height = max(self._min_height, min(content_height, self._max_height))
        else:
            target_height = 0
        anim = QPropertyAnimation(self.scroll_area, b"maximumHeight")
        anim.setDuration(300)
        anim.setStartValue(self.scroll_area.maximumHeight())
        anim.setEndValue(target_height)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        anim.finished.connect(self._on_animation_finished)
        self._current_anim = anim

    def _on_animation_finished(self):
        self.updateGeometry()
        self.scroll_area.widget().updateGeometry()
        window = self.window()
        if window:
            window.adjustSize()

    def _update_icon(self):
        icon_path = self.collapse_icon if self.is_expanded else self.expand_icon
        pixmap = QPixmap(icon_path).scaled(
            24, 24, 
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.state_icon.setPixmap(pixmap)

    def set_scroll_content(self, widget: QWidget):
        self.scroll_area.widget().layout().addWidget(widget)

    def add_component(self, component: QWidget, alignment: Qt.AlignmentFlag = None) -> None:
        layout = self.scroll_area.widget().layout()
        if alignment is None:
            layout.addWidget(component)
        else:
            layout.addWidget(component, alignment)

    def text(self) -> str:
        return self.text_label.text()

    def set_height_limits(self, min_h: int, max_h: int):
        self._min_height = min_h
        self._max_height = max_h
        if self.is_expanded:
            content_height = self.scroll_area.widget().sizeHint().height()
            clamped = max(self._min_height, min(content_height, self._max_height))
            self.scroll_area.setMaximumHeight(clamped)
