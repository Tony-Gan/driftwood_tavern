from typing import List

from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon

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
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setFixedWidth(600)
        self.setMaximumHeight(1000)

        self.dialog_type = dialog_type
        
        self._init_title_bar(title)
        self._init_scroll_area(layout_type)
        self._init_button_bar(button1, button2)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        main_layout.addWidget(self.title_bar, stretch=1)
        main_layout.addWidget(self.container, stretch=5)
        main_layout.addWidget(self.button_bar, stretch=1)
        
        self.setLayout(main_layout)

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
        self.container = DTBaseScrollArea(parent=self, layout_type=layout_type)
        self.container.setStyleSheet("""
                background-color: #FFFFFF;
                color: black;
            """)

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
                    width=300,
                    font=NonSerifBlackLarge,
                    height=60,
                    radius=0
                )
                button.clicked.connect(handler)
                self.button_bar.add_component('btn', button)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)
        