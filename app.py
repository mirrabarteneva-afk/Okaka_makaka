from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve
from ui.controls_panel import Leftpanel
from ui.table_view import Main_panel
from PyQt6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QSplitter,
    QPushButton,
    QScrollArea,
    QSizePolicy
)


QWIDGETSIZE_MAX = 16777215

class Okaka_makaka(QMainWindow):
    def __init__(self, assets_path):
        super().__init__()
        self.assets_path = assets_path
        self._is_left_visible = True
        self.icon_show = QIcon(str(self.assets_path / "assets" / "open.png"))
        self.icon_hide = QIcon(str(self.assets_path / "assets" / "close.png"))
        self.max_width_panel = 900
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Okaka_Makaka")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)
        splitter.setChildrenCollapsible(False)


        self.left_panel = Leftpanel(self.assets_path)
        new_layout = self.left_panel.layout()

        content_widget = QWidget()
        content_widget.setLayout(new_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(content_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        splitter.addWidget(self.scroll_area)

        dummy_right = QWidget()
        dummy_layout = QVBoxLayout(dummy_right)
        splitter.addWidget(dummy_right)

        splitter.setSizes([350, 850])

        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(40, 40)
        self.toggle_btn.setObjectName('toggle_btn')
        self.toggle_btn.setIcon(self.icon_hide)
        self.toggle_btn.setIconSize(QSize(24, 24))
        self.toggle_btn.clicked.connect(self.toggle_panel)

        main_layout.addWidget(splitter)
        main_layout.addWidget(self.toggle_btn)

    def toggle_panel(self):
        self._is_left_visible = not self._is_left_visible

        if getattr(self, '_panel_anim', None) is not None:
            self._panel_anim.stop()

        panel = self.scroll_area

        if self._is_left_visible:
            panel.setVisible(True)
            panel.setMinimumWidth(0)
            target = getattr(self, '_panel_width_before', self.max_width_panel)
            self._animate_panel_width(target, on_finish=lambda: panel.setMaximumWidth(QWIDGETSIZE_MAX))
            self.toggle_btn.setIcon(self.icon_hide)
        else:
            self._panel_width_before = max(panel.width(), 200)
            self._animate_panel_width(0, on_finish=panel.hide)
            self.toggle_btn.setIcon(self.icon_show)
            self.left_panel.setMinimumWidth(0)


    def _animate_panel_width(self, target, on_finish=None):
        panel = self.scroll_area

        self._panel_anim = QPropertyAnimation(panel, b"maximumWidth", self)
        self._panel_anim.setDuration(300)
        self._panel_anim.setStartValue(panel.width())
        self._panel_anim.setEndValue(target)
        self._panel_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        if on_finish is not None:
            self._panel_anim.finished.connect(on_finish)

        self._panel_anim.start()