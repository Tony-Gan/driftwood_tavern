from PyQt6.QtCore import Qt

from core.frames.basic_info_frame import BasicInfoBar
from core.frames.main_container import MainContainer
from core.frames.progress_bar import ProgressBar
from models.character import Character
from ui.dt_base_frame import DTBaseFrame


class DTCharacterBuilder(DTBaseFrame):
    def __init__(self, parent):
        self.p_data = Character()
        super().__init__(parent=parent)

    def _setup_content(self):
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.progress_bar = ProgressBar(self)
        self.basic_info_bar = BasicInfoBar(self)
        self.main_container = MainContainer(self, self.p_data)

        self.add_child('progress_bar', self.progress_bar)
        self.add_child('basic_info_bar', self.basic_info_bar)
        self.add_child('main_container', self.main_container)
