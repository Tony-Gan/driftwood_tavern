from PyQt6.QtWidgets import QStackedWidget, QWidget


class DTStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widgets = []

    def addWidget(self, widget: QWidget) -> int:
        index = super().addWidget(widget)
        self.widgets.append(widget)
        return index
    
    def insertWidget(self, index: int, widget: QWidget) -> int:
        new_index = super().insertWidget(index, widget)
        self.widgets.insert(index, widget)
        return new_index

    def removeWidget(self, widget: QWidget) -> None:
        if widget in self.widgets:
            self.widgets.remove(widget)
        super().removeWidget(widget)

    def clearWidgets(self) -> None:
        for widget in self.widgets[:]:
            super().removeWidget(widget)
            widget.deleteLater() 
        self.widgets.clear()

    def getWidgetByName(self, name: str) -> QWidget:
        for widget in self.widgets:
            if widget.objectName() == name:
                return widget
        return None
