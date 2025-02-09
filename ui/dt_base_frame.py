from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLayout
from PyQt6.QtCore import pyqtSignal, Qt

from ui.interfaces.idt_container import IDTContainer


class DTBaseFrame(QFrame, IDTContainer):
    values_changed = pyqtSignal(dict)

    def __init__(self, parent, layout_type: type[QLayout] = QVBoxLayout, 
                 alignment=Qt.AlignmentFlag.AlignCenter):
        super().__init__(parent)
        self.parent = parent
        self.main_layout = layout_type(self)
        self.main_layout.setAlignment(alignment)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        if not issubclass(layout_type, QLayout):
            raise TypeError(f"Invalid layout_type: {layout_type}. Expected a subclass of QLayout.")

        self.init_interface()

        self.setFrameShape(QFrame.Shape.NoFrame)
        self._setup_content()

    def _setup_content(self) -> None:
        pass
