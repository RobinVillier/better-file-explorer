from typing import Optional

from PySide2 import QtWidgets, QtCore, QtGui

from BetterFileExplorer import main
from BetterFileExplorer.core import load
from BetterFileExplorer.core import logic_settings
from BetterFileExplorer.core import logic_save_as
from BetterFileExplorer.config import settings
from BetterFileExplorer.widgets import custom_frame


class SaveAsUI(QtWidgets.QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(SaveAsUI, self).__init__(parent)

        self.project_path = load.get_project_path()
        self.current_environment = load.get_current_environment()

        self.setWindowTitle(f"SaveAs  |  {settings.APP_NAME}  |  v{settings.VERSION}")
        self.setMinimumSize(400, 0)
        # self.resize(400, 650)
        self.setWindowIcon(QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/save_black_icon.svg"))

        stylesheet = load.load_qss_with_fixed_urls(rf"{settings.ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.create_widgets()
        self.create_master_layout()

        logic_save_as.update_environment(self)
        logic_save_as.update_file_name_preview(self)

    # UI
    def create_widgets(self):
        self.create_header_widgets()
        self.create_save_settings_widgets()
        self.create_save_btn_widgets()

    def create_header_widgets(self):
        self.environment_title_label = QtWidgets.QLabel("Current Environment")
        self.environment_title_label.setObjectName("SettingsTitles")

        self.reload_env_button = QtWidgets.QPushButton()
        self.reload_env_button.setObjectName("RoundedButton")
        self.reload_env_button.setFixedWidth(30)
        self.reload_env_button.setIcon(QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/reload_white_icon.svg"))
        self.reload_button_clicked()

        self.current_env_label = QtWidgets.QLabel()
        self.current_env_label.setObjectName("Bold")
        self.current_env_label.setAlignment(QtCore.Qt.AlignCenter)

    def create_save_settings_widgets(self):
        self.save_settings_label = QtWidgets.QLabel("Save Settings")
        self.save_settings_label.setObjectName("SettingsTitles")
        self.save_settings_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.title_name_preview_label = QtWidgets.QLabel("File Name Preview : ")
        self.title_name_preview_label.setObjectName("Bold")

        self.file_name_preview_label = QtWidgets.QLabel("")
        self.file_name_preview_label.setObjectName("Bold")

        self.version_up_rb = QtWidgets.QRadioButton("Version Up")
        self.version_up_rb.setChecked(True)
        self.publish_rb = QtWidgets.QRadioButton("Publish")

        self.v_up_radio_button()

    def create_save_btn_widgets(self):
        self.save_button = QtWidgets.QPushButton("Save As")
        self.save_button.setObjectName("RoundedButton")
        self.save_button_clicked()

    def create_master_layout(self):
        _master_layout = QtWidgets.QVBoxLayout(self)
        _master_layout.setContentsMargins(0, 0, 0, 6)
        _master_layout.setSpacing(0)

        self.create_header_layout()
        self.create_file_name_layout()
        self.create_save_button_layout()
        _master_layout.addWidget(self.header_frame)
        _master_layout.addWidget(self.file_name_frame)
        _master_layout.addWidget(self.save_button_layout)

    def create_header_layout(self):
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addStretch(1)
        header_layout.addWidget(self.environment_title_label)
        header_layout.addWidget(self.reload_env_button)
        header_layout.addStretch(1)

        self.header_frame = custom_frame.Frame(name="Section", fixed_height=70)
        self.header_frame.content_layout().addLayout(header_layout)
        self.header_frame.content_layout().addWidget(self.current_env_label)

    def create_file_name_layout(self):
        file_preview_labels_layout = QtWidgets.QHBoxLayout()
        file_preview_labels_layout.setAlignment(QtCore.Qt.AlignCenter)
        file_preview_labels_layout.addWidget(self.title_name_preview_label)
        file_preview_labels_layout.addWidget(self.file_name_preview_label)

        radio_buttons_layout = QtWidgets.QHBoxLayout()
        radio_buttons_layout.setAlignment(QtCore.Qt.AlignCenter)
        radio_buttons_layout.addWidget(self.version_up_rb)
        radio_buttons_layout.addWidget(self.publish_rb)

        center_layout = QtWidgets.QVBoxLayout()
        center_layout.addWidget(self.save_settings_label)
        center_layout.addSpacing(0)
        center_layout.addLayout(file_preview_labels_layout)
        center_layout.addSpacing(5)
        center_layout.addLayout(radio_buttons_layout)
        center_layout.addSpacing(5)

        self.file_name_frame = custom_frame.Frame(name="Section")
        self.file_name_frame.content_layout().addLayout(center_layout)

    def create_save_button_layout(self):
        self.save_button_layout = custom_frame.Frame(name="Section", fixed_height=43)
        self.save_button_layout.content_layout().addWidget(self.save_button)

    # WIDGETS
    @staticmethod
    def create_divider():
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)

        return divider

    # SIGNALS
    def reload_button_clicked(self):
        self.reload_env_button.clicked.connect(lambda: logic_save_as.update_environment(self))
        self.reload_env_button.clicked.connect(lambda: logic_save_as.update_file_name_preview(self))

    def save_button_clicked(self):
        self.save_button.clicked.connect(lambda: logic_save_as.save_file(self))
        self.save_button.clicked.connect(lambda: logic_save_as.update_file_name_preview(self))
        self.save_button.clicked.connect(self.close)

    def v_up_radio_button(self):
        self.version_up_rb.toggled.connect(lambda: logic_save_as.update_file_name_preview(self))
