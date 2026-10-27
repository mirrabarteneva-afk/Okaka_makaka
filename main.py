import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
import app

def load_style(qss_name: str) -> str:
    path = Path(__file__).resolve().parent
    qss_path = path / 'styles' / qss_name
    with open(qss_path, 'r', encoding='utf-8') as style:
        return style.read()

if __name__ == '__main__':
    app_instance = QApplication(sys.argv)
    style = load_style('theme.qss')
    app_instance.setStyleSheet(style)
    assets_path = Path(__file__).resolve().parent
    ex = app.Okaka_makaka(assets_path)
    ex.showMaximized()
    sys.exit(app_instance.exec())