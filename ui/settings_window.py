from typing import Optional

from PySide2 import QtWidgets, QtCore, QtGui

from BetterFileExplorer import main
from BetterFileExplorer.core import load
from BetterFileExplorer.core import logic_settings
from BetterFileExplorer.config import settings


class SettingsUI(QtWidgets.QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(SettingsUI, self).__init__(parent)

        self.project_path = load.get_project_path()

        self.setWindowTitle(f"Settings  |  {settings.APP_NAME}  |  v{settings.VERSION}")
        self.setMinimumSize(400, 0)
        self.resize(400, 700)
        self.setWindowIcon(QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/settings_black.svg"))

        stylesheet = load.load_qss_with_fixed_urls(rf"{settings.ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.create_widgets()
        self.create_master_layout()

    # UI
    def create_widgets(self):
        self.create_settings_widgets()
        self.create_folder_hierarchy_widgets()
        self.create_tab_widget()

    def create_tab_widget(self):
        settings_tab = QtWidgets.QWidget()
        settings_tab.setLayout(self.settings_layout)

        folder_hierarchy_tab = QtWidgets.QWidget()
        folder_hierarchy_tab.setLayout(self.folder_hierarchy_layout)

        self.tabs_widget = QtWidgets.QTabWidget()
        self.tabs_widget.addTab(settings_tab, "Settings")
        self.tabs_widget.addTab(folder_hierarchy_tab, "Template Hierarchy")

    def create_settings_widgets(self):
        # Label
        project_path_label = QtWidgets.QLabel("Project Path :")
        project_path_label.setObjectName("SettingsTitles")

        # Line Edit
        self.project_path_line_edit = QtWidgets.QLineEdit()
        self.project_path_line_edit.setText(self.project_path)

        # Select Folder Button
        select_folder_button = QtWidgets.QPushButton()
        select_folder_button.setObjectName("RoundedButton")
        select_folder_button.setFixedWidth(30)
        select_folder_button.setIcon(QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/folder_white.png"))

        select_folder_button.clicked.connect(
            lambda: logic_settings.get_user_directory(self)
        )

        # Divider 1
        divider_1 = self.create_divider()

        # Default task label and combobox
        default_task_label = QtWidgets.QLabel("Default Task :")
        default_task_label.setObjectName("SettingsTitles")

        self.default_task_combo = QtWidgets.QComboBox()

        task_list = logic_settings.get_default_task_list()
        self.default_task_combo.addItems(task_list)
        self.default_task_combo.setCurrentText(load.get_default_task())

        # Divider 2
        divider_2 = self.create_divider()

        # Recent File Saved Amount
        recent_files_label = QtWidgets.QLabel("Amount Of Recent Files Saved :")
        recent_files_label.setObjectName("SettingsTitles")

        self.recent_files_spinbox = QtWidgets.QSpinBox()
        self.recent_files_spinbox.setMinimum(1)
        self.recent_files_spinbox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        recent_files_amount_dict = load.open_json(settings.SETTINGS_PATH)
        self.recent_files_spinbox.setValue(int(recent_files_amount_dict.get("recent_files_amount", 10)))

        # Save Button
        save_settings_buttons = QtWidgets.QPushButton("Save and Close")
        save_settings_buttons.setObjectName("RoundedButton")
        save_settings_buttons.setFixedWidth(100)
        save_settings_buttons.clicked.connect(lambda: logic_settings.save_settings(self))
        save_settings_buttons.clicked.connect(self.close)

        # Save Btn Layout
        self.save_btn_layout = QtWidgets.QHBoxLayout()
        self.save_btn_layout.addWidget(save_settings_buttons)
        self.save_btn_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Project Path Line Edit Layout
        project_path_layout = QtWidgets.QHBoxLayout()
        project_path_layout.addWidget(self.project_path_line_edit)
        project_path_layout.addWidget(select_folder_button)

        # Amount Of Recent Files Saved Layout
        recent_files_layout = QtWidgets.QHBoxLayout()
        recent_files_layout.addWidget(recent_files_label)
        recent_files_layout.addSpacing(5)
        recent_files_layout.addWidget(self.recent_files_spinbox)
        recent_files_layout.addStretch(1)

        # Settings Tab Layout
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.setAlignment(QtCore.Qt.AlignTop)

        self.settings_layout.addWidget(project_path_label)
        self.settings_layout.addLayout(project_path_layout)

        self.settings_layout.addSpacing(5)
        self.settings_layout.addWidget(divider_1)
        self.settings_layout.addSpacing(5)

        self.settings_layout.addWidget(default_task_label)
        self.settings_layout.addWidget(self.default_task_combo)

        self.settings_layout.addSpacing(5)
        self.settings_layout.addWidget(divider_2)
        self.settings_layout.addSpacing(5)

        self.settings_layout.addLayout(recent_files_layout)

    def create_folder_hierarchy_widgets(self):
        # Label
        folder_hierarchy_label = QtWidgets.QLabel("Template Folder Hierarchy :")
        folder_hierarchy_label.setObjectName("SettingsTitles")

        # Combobox
        icon_profile_button = QtWidgets.QPushButton()
        icon_profile_button.setObjectName("RoundedButton")
        icon_profile_button.setFixedWidth(30)
        icon_profile_button.setIcon(QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/new_white.png"))

        icon_profile_button.clicked.connect(main.launch_new_profile)

        select_profile_combo = QtWidgets.QComboBox()
        logic_settings.populate_profile_drop_down(select_profile_combo)
        select_profile_combo.setCurrentText(settings.get_current_hierarchy_profile())
        select_profile_combo.currentTextChanged.connect(
            lambda: logic_settings.update_current_profile(select_profile_combo)
        )
        select_profile_combo.currentTextChanged.connect(
            lambda: logic_settings.populate_folder_hierarchy_tree(self.folder_hierarchy_tree_widget)
        )

        # Tree Widget
        self.folder_hierarchy_tree_widget = QtWidgets.QTreeWidget()
        self.folder_hierarchy_tree_widget.setColumnCount(1)
        self.folder_hierarchy_tree_widget.setHeaderHidden(True)
        self.folder_hierarchy_tree_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.folder_hierarchy_tree_widget.customContextMenuRequested.connect(self.open_menu)

        logic_settings.populate_folder_hierarchy_tree(self.folder_hierarchy_tree_widget)

        # Updated widgets when new_profile window closes
        icon_profile_button.clicked.connect(
            lambda: self._update_window_widgets(select_profile_combo, self.folder_hierarchy_tree_widget)
        )

        # Layouts
        title_layout = QtWidgets.QHBoxLayout()
        title_layout.addWidget(folder_hierarchy_label)
        title_layout.addWidget(icon_profile_button)
        title_layout.addWidget(select_profile_combo)

        self.folder_hierarchy_layout = QtWidgets.QVBoxLayout()
        self.folder_hierarchy_layout.addLayout(title_layout)
        self.folder_hierarchy_layout.addWidget(self.folder_hierarchy_tree_widget)

    def create_master_layout(self):
        master_layout = QtWidgets.QVBoxLayout(self)
        master_layout.setContentsMargins(10, 10, 10, 10)
        master_layout.setSpacing(5)
        master_layout.setAlignment(QtCore.Qt.AlignCenter)

        master_layout.addWidget(self.tabs_widget)
        master_layout.addLayout(self.save_btn_layout)

    @staticmethod
    def _update_window_widgets(combo_box, folder_hierarchy):
        logic_settings.populate_profile_drop_down(widget=combo_box)
        logic_settings.populate_folder_hierarchy_tree(tree_widget=folder_hierarchy)

    # WIDGETS
    @staticmethod
    def create_divider():
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFrameShadow(QtWidgets.QFrame.Sunken)

        return divider

    # SIGNALS
    def open_menu(self, position):
        selected_item = self.folder_hierarchy_tree_widget.itemAt(position)

        if selected_item is None:
            return

        selected_item_role = selected_item.data(0, QtCore.Qt.UserRole).get("role")
        rename_action = None
        delete_action = None

        menu = QtWidgets.QMenu()
        add_action = menu.addAction("New Folder")
        if not selected_item_role:
            rename_action = menu.addAction("Rename")
            delete_action = menu.addAction("Delete")

        action = menu.exec_(self.folder_hierarchy_tree_widget.viewport().mapToGlobal(position))

        if action == add_action:
            logic_settings.create_folder(self, selected_item, self.folder_hierarchy_tree_widget)
        elif not selected_item_role:
            if action == rename_action:
                logic_settings.rename_folder(self, selected_item, self.folder_hierarchy_tree_widget)
            elif action == delete_action:
                logic_settings.delete_folder(self, selected_item, self.folder_hierarchy_tree_widget)
