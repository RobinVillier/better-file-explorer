from typing import Optional

from PySide2 import QtWidgets, QtCore, QtGui

from BetterFileExplorer.config import settings
from BetterFileExplorer.core import load
from BetterFileExplorer.core import logic_selector
from BetterFileExplorer.widgets import custom_frame


class NewContentUI(QtWidgets.QDialog):
    def __init__(self,
                 parent: Optional[QtWidgets.QWidget] = None,
                 role="",
                 main_window: QtWidgets.QDialog = None):
        super(NewContentUI, self).__init__(parent)
        self.role = role
        self.main_window = main_window

        self.setWindowTitle(
            f"Create New {self.role.capitalize()} Folder |  {settings.APP_NAME}  |  v{settings.VERSION}"
        )
        self.setWindowIcon(QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/folder_black.png"))

        stylesheet = load.load_qss_with_fixed_urls(rf"{settings.ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.create_widgets()
        self.create_master_layout()

    def create_widgets(self):
        new_profile_label = QtWidgets.QLabel(f"New {self.role.capitalize()} Folder:")
        new_profile_label.setObjectName("SettingsTitles")

        new_profile_line_edit = QtWidgets.QLineEdit()
        new_profile_line_edit.returnPressed.connect(
            lambda: logic_selector.create_client_hierarchy_from_template(self, self.role, new_profile_line_edit, self.main_window)
        )

        create_button = QtWidgets.QPushButton("Create")
        create_button.setObjectName("RoundedButton")

        create_button.clicked.connect(
            lambda: logic_selector.create_client_hierarchy_from_template(self, self.role, new_profile_line_edit, self.main_window)
        )

        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.setObjectName("RoundedButton")

        cancel_button.clicked.connect(self.close)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(create_button)
        buttons_layout.addWidget(cancel_button)

        self.create_profile_frame = custom_frame.Frame(name="NewProfile")
        self.create_profile_frame.content_layout().addWidget(new_profile_label)
        self.create_profile_frame.content_layout().addWidget(new_profile_line_edit)
        self.create_profile_frame.content_layout().addLayout(buttons_layout)

    def create_master_layout(self):
        _master_layout = QtWidgets.QVBoxLayout(self)
        _master_layout.setContentsMargins(0, 0, 0, 0)
        _master_layout.setSpacing(0)
        _master_layout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        _master_layout.addWidget(self.create_profile_frame)
