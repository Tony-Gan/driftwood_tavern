from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

from utils.dt_fonts import NonSerifMediumTitle, NonSerifLightSub

class DTTitleLabel(QLabel):
    def __init__(self, text="", width=80, parent=None):
        super().__init__(text, parent)

        self.setStyleSheet("color: black;")
        self.setContentsMargins(0, 12, 0, 5)
        self.setFont(NonSerifMediumTitle)
        self.setFixedWidth(width)


class DTNormalLabel(QLabel):
    def __init__(self, text="", width=80, parent=None):
        super().__init__(text, parent)

        self.setStyleSheet("color: black;")
        self.setContentsMargins(0, 3, 0, 3)
        self.setFont(NonSerifLightSub)
        self.setWordWrap(True)
        self.setFixedWidth(width)
