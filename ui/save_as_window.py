from typing import Optional

from PySide2 import QtWidgets, QtCore, QtGui

from BetterFileExplorer import main
from BetterFileExplorer.core import load
from BetterFileExplorer.core import logic_settings
from BetterFileExplorer.config import settings
from BetterFileExplorer.widgets import custom_frame


class SaveAsUI(QtWidgets.QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(SaveAsUI, self).__init__(parent)

        self.project_path = load.get_project_path()
        self.current_environment = load.get_current_environment()

        self.setWindowTitle(f"SaveAs  |  {settings.APP_NAME}  |  v{settings.VERSION}")
        self.setMinimumSize(400, 0)
        self.resize(400, 650)
        self.setWindowIcon(QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/save_black_icon.svg"))

        stylesheet = load.load_qss_with_fixed_urls(rf"{settings.ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.create_widgets()
        self.create_master_layout()

    # UI
    def create_widgets(self):
        self.create_header_widgets()

    def create_header_widgets(self):
        self.environment_label = QtWidgets.QLabel("Current Environment")
        self.environment_label.setObjectName("SettingsTitles")

        self.reload_env_button = QtWidgets.QPushButton()
        self.reload_env_button.setObjectName("RoundedButton")
        self.reload_env_button.setFixedWidth(30)
        self.reload_env_button.setIcon(QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/reload_white_icon.svg"))

    def create_header_layout(self):
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addStretch(1)
        header_layout.addWidget(self.environment_label)
        header_layout.addWidget(self.reload_env_button)
        header_layout.addStretch(1)

        self.selector_frame = custom_frame.Frame(name="Section")
        self.selector_frame.content_layout().addLayout(header_layout)

    def create_master_layout(self):
        _master_layout = QtWidgets.QVBoxLayout(self)
        _master_layout.setContentsMargins(10, 10, 10, 10)
        _master_layout.setSpacing(5)

        self.create_header_layout()
        _master_layout.addWidget(self.selector_frame)

    # WIDGETS
    @staticmethod
    def create_divider():
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)

        return divider

    # SIGNALS
