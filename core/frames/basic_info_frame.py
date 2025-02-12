from PyQt6.QtWidgets import QLabel, QHBoxLayout, QStackedLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from ui.dt_base_frame import DTBaseFrame
from ui.dt_value_entry import DTValueEntry
from utils.dt_fonts import NonSerifLight, NonSerifNormal
from utils.dt_utils import DTUtils


class BasicInfoBar(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(layout_type=QHBoxLayout, parent=parent)

    def _setup_content(self):
        self.setFixedHeight(80)
        self.main_layout.setSpacing(40)

        self.avatar_frame = AvatarFrame(self)
        self.info_frame = InfoFrame(self)

        pixmap_previous = QPixmap(DTUtils.resource_path("resources/icons/previous.png"))
        pixmap_previous = pixmap_previous.scaled(50, 50, 
                                      Qt.AspectRatioMode.KeepAspectRatio, 
                                      Qt.TransformationMode.SmoothTransformation)
        
        pixmap_next = QPixmap(DTUtils.resource_path("resources/icons/next.png"))
        pixmap_next = pixmap_next.scaled(50, 50, 
                                      Qt.AspectRatioMode.KeepAspectRatio, 
                                      Qt.TransformationMode.SmoothTransformation)
        
        self.previous = QLabel(self)
        self.previous.setPixmap(pixmap_previous)
        self.previous.mousePressEvent = self._on_previous_clicked

        self.next = QLabel(self)
        self.next.setPixmap(pixmap_next)
        self.next.mousePressEvent = self._on_next_clicked
        
        self.main_layout.addStretch()
        self.main_layout.addStretch()
        self.add_component('previous', self.previous)
        self.main_layout.addStretch()
        self.add_child('avatar_frame', self.avatar_frame)
        self.add_child('info_frame', self.info_frame)
        self.main_layout.addStretch()
        self.add_component('next', self.next)
        self.main_layout.addStretch()
        self.main_layout.addStretch()

    def _on_previous_clicked(self, event):
        self.parent.main_container.switch_to_previous()

    def _on_next_clicked(self, event):
        self.parent.main_container.switch_to_next()


class AvatarFrame(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(layout_type=QStackedLayout, parent=parent)

    def _setup_content(self):
        self.setFixedSize(60, 60)
        self.setStyleSheet("""
            QFrame {
                border: 1px dashed black;
            }
        """)

        self.silhouette_label = QLabel(self)
        pixmap_sil = QPixmap(DTUtils.resource_path("resources/icons/default_avatar.png"))
        pixmap_sil = pixmap_sil.scaled(self.width() - 10, self.height() - 10, 
                                      Qt.AspectRatioMode.KeepAspectRatio, 
                                      Qt.TransformationMode.SmoothTransformation)
        self.silhouette_label.setPixmap(pixmap_sil)
        self.silhouette_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_component('silhouette_label', self.silhouette_label)

        self.plus_label = QLabel(self)
        pixmap_plus = QPixmap(DTUtils.resource_path("resources/icons/upload.png"))
        pixmap_plus = pixmap_plus.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.TransformationMode.SmoothTransformation)
        self.plus_label.setPixmap(pixmap_plus)
        self.plus_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_component('plus_label', self.plus_label)

        self.main_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)


class InfoFrame(DTBaseFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)

    def _setup_content(self):
        self.setFixedHeight(70)
        self.setFixedWidth(140)
        self.char_name = DTValueEntry(
            label_text='角色名',
            label_size=50,
            label_font=NonSerifNormal,
            value_size=80,
            value_font=NonSerifLight
        )

        self.pl_name = DTValueEntry(
            label_text='玩家名',
            label_size=50,
            label_font=NonSerifNormal,
            value_size=80,
            value_font=NonSerifLight
        )

        self.add_component('char_name', self.char_name)
        self.add_component('pl_name', self.pl_name)
        