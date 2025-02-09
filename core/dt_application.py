from PyQt6.QtWidgets import QApplication


class DTApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        pass
    #     self._message_bar = None

    # @property
    # def message_bar(self) -> DTMessageBar:
    #     return self._message_bar
    
    # @message_bar.setter
    # def message_bar(self, bar: DTMessageBar):
    #     self._message_bar = bar

    # def show_message(self, message: str, display_time: int=2000, colour: str='green'):
    #     if self._message_bar:
    #         self._message_bar.show_message(message, display_time, colour)

    @staticmethod
    def instance() -> 'DTApplication':
        return QApplication.instance()