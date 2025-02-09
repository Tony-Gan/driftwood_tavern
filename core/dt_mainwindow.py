from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon, QPainter, QPixmap

from core.dt_application import DTApplication
from core.dt_homepage import DTHomePage
from core.dt_character_builder import DTCharacterBuilder
from utils.dt_utils import DTUtils


class DTMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = DTApplication.instance()
        self.setWindowTitle('沉木酒馆')
        self.setWindowIcon(QIcon(DTUtils.resource_path('resources/icons/app.png')))
        self.background_image = QPixmap(DTUtils.resource_path('resources/images/background.png'))

        self.setGeometry(100, 100, 1600, 1000)

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)
        
        self.home_page = DTHomePage(self)
        self.builder_page = DTCharacterBuilder(self)
        # self.pageManageCharacter = ManageCharacterPage(self)

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.builder_page)
        # self.stack.addWidget(self.pageManageCharacter)
        
        self.stack.setCurrentWidget(self.home_page)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)
        super().paintEvent(event)

    def switch_to_home(self):
        self.stack.setCurrentWidget(self.home_page)

    def switch_to_create_character(self):
        self.stack.setCurrentWidget(self.builder_page)

    def switch_to_manage_character(self):
        print("2")
        # self.stack.setCurrentWidget(self.pageManageCharacter)
