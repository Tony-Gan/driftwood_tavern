import os
import sys

from PyQt6.QtGui import QFontDatabase

from core.dt_application import DTApplication
from core.dt_mainwindow import DTMainWindow
from utils.dt_utils import DTUtils


def main():
    app = DTApplication(sys.argv)

    load_font()

    window = DTMainWindow()
    window.show()

    sys.exit(app.exec())

def load_font():
    """
    - Noto Serif SC SemiBold
    - Noto Sans SC Medium
    - Noto Sans SC
    - Noto Serif SC
    - Noto Sans SC Light
    - Noto Sans SC Black
    - Noto Serif SC ExtraLight
    - Noto Serif SC Light
    - Noto Sans SC ExtraBold
    - Noto Sans SC Thin
    - Noto Sans SC SemiBold
    - Noto Sans SC ExtraLight
    - Noto Serif SC Medium
    - 三极花朝体 粗
    """
    fonts_dir = DTUtils.resource_path("resources/fonts")

    for root, _, files in os.walk(fonts_dir):
        for file in files:
            if file.endswith(('.ttf', '.otf')):
                font_path = os.path.join(root, file)
                QFontDatabase.addApplicationFont(font_path)

if __name__ == '__main__':
    main()
