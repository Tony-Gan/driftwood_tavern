from typing import List

from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon

from core.dt_application import DTApplication
from ui.dt_base_button import DTStandardButton
from ui.dt_base_frame import DTBaseFrame
from ui.dt_base_scroll_area import DTBaseScrollArea
from ui.interfaces.idt_container import IDTContainer
from utils.dt_fonts import NonSerifBlackLarge
from utils.dt_utils import DTUtils


class DTBaseDialog(QDialog, IDTContainer):
    closed = pyqtSignal()

    def __init__(
            self, 
            title: str, 
            layout_type: type[QLayout] = QVBoxLayout,
            button1: List = None,
            button2: List = None,
            dialog_type: str = "default",
            parent=None
        ):
        super().__init__(parent)
        self.init_interface()
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedWidth(500)
        self.setMaximumHeight(1000)
        self.dialog_type = dialog_type
        self.old_pos = None
        self.mask = None
        
        self._init_title_bar(title)
        self._init_scroll_area(layout_type)
        self._init_button_bar(button1, button2)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.container)
        self.main_layout.addWidget(self.button_bar)
        
        self.setLayout(self.main_layout)

    def _init_title_bar(self, title: str):
        self.title_bar = DTBaseFrame(layout_type=QHBoxLayout, parent=self)
        self.title_bar.setFixedHeight(60)
        self.title_bar.main_layout.setContentsMargins(15, 0, 15, 0)
        if self.dialog_type == 'warning':
            self.title_bar.setStyleSheet("""
                background-color: #E40712;
                color: white;
            """)
        else:
            self.title_bar.setStyleSheet("""
                background-color: #232B2F;
                color: white;
            """)
        
        lbl_title = QLabel(title)
        lbl_title.setFont(NonSerifBlackLarge)
        
        btn_close = QPushButton()
        btn_close.setIcon(QIcon(DTUtils.resource_path("resources/icons/close.png")))
        btn_close.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                padding: 5px;
            }
        """)
        btn_close.clicked.connect(self.reject)

        self.title_bar.add_component('lbl', lbl_title)
        self.title_bar.main_layout.addStretch()
        self.title_bar.add_component('btn', btn_close)

    def _init_scroll_area(self, layout_type: type[QLayout]):
        self.container = DTBaseScrollArea(parent=self, layout_type=layout_type, auto_adjust_height=True)
        self.container.setContentsMargins(20, 20, 20, 20)
        self.container.setStyleSheet("""
                    background-color: #FFFFFF;
                    color: black;
                """)
        self.container.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.container.setMaximumHeight(800)

    def _init_button_bar(self, button1: List, button2: List):
        self.button_bar = DTBaseFrame(layout_type=QHBoxLayout, parent=self)
        self.button_bar.setFixedHeight(60)
    
        if not button1 and not button2:
            button1 = ["OK", self.accept]
            button2 = ["Cancel", self.reject]
        
        for btn_config in [button1, button2]:
            if btn_config:
                text, handler = btn_config
                button = DTStandardButton(
                    text=text,
                    width=250,
                    font=NonSerifBlackLarge,
                    height=60,
                    radius=0
                )
                button.clicked.connect(handler)
                self.button_bar.add_component('btn', button)

    def add_component(self, name, component):
        self.container.add_component(name, component)
    
    def add_child(self, name, child, alignment = None):
        self.container.add_child(name, child)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.old_pos and (event.buttons() & Qt.MouseButton.LeftButton):
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.old_pos = None
        super().mouseReleaseEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        parent = self.parent() or DTApplication.activeWindow()
        if parent:
            self.mask = QWidget(parent)
            self.mask.setStyleSheet("background-color: rgba(128, 128, 128, 0.5);")
            self.mask.setGeometry(parent.rect())
            self.mask.show()
            self.raise_()

    def cleanup_mask(self):
        if self.mask:
            self.mask.hide()
            self.mask.deleteLater()
            self.mask = None

    def accept(self):
        self.cleanup_mask()
        super().accept()

    def reject(self):
        self.cleanup_mask()
        super().reject()

    def closeEvent(self, event):
        self.cleanup_mask()
        self.closed.emit()
        super().closeEvent(event)
