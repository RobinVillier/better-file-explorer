from typing import Optional

from PySide2 import QtWidgets, QtCore, QtGui

from BetterFileExplorer.config import settings
from BetterFileExplorer.core import load
from BetterFileExplorer.core import logic_selector
from BetterFileExplorer.core import logic_folder_content

from BetterFileExplorer.widgets import menu_bar
from BetterFileExplorer.widgets import custom_frame
from BetterFileExplorer.widgets import labeled_combo_box
from BetterFileExplorer.widgets import rounded_item_delegate as rid


class BetterFileExplorerUI(QtWidgets.QDialog):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super(BetterFileExplorerUI, self).__init__(parent)

        self.project_path = load.get_project_path()

        self.setWindowTitle(f"{settings.APP_NAME}  |  v{settings.VERSION}")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setMinimumSize(0, 0)
        self.resize(500, 650)
        self.setWindowIcon(QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/folder_black.png"))

        stylesheet = load.load_qss_with_fixed_urls(rf"{settings.ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.create_widgets()
        self.create_master_layout()

        current_env = load.get_current_environment()
        logic_selector.update_selector_on_env(self, current_env)

    # UI
    def create_widgets(self):
        self.menu_bar = menu_bar.MenuBar(self)
        self.create_selector_section()
        self.create_folder_content_list_section()
        self.create_bottom_section_tabs()

    def create_master_layout(self):
        _master_layout = QtWidgets.QVBoxLayout(self)
        _master_layout.setContentsMargins(0, 0, 0, 6)
        _master_layout.setSpacing(0)
        _master_layout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        _master_layout.addWidget(self.menu_bar)
        _master_layout.addWidget(self.selector_frame)
        _master_layout.addWidget(self.folder_content_frame)
        _master_layout.addWidget(self.recent_files_frame)

    def create_selector_section(self):
        def make_row(left_label, left_attr, right_label, right_attr):
            layout = QtWidgets.QHBoxLayout()

            left = labeled_combo_box.LabeledComboBox(left_label)
            right = labeled_combo_box.LabeledComboBox(right_label)

            layout.addWidget(left, 1)
            layout.addWidget(right, 1)

            setattr(self, left_attr, left.combobox)
            setattr(self, right_attr, right.combobox)

            return layout

        self.selector_frame = custom_frame.Frame(name="Section")

        client_project_layout = make_row("Client", "client_combo", "Project", "project_combo")  # self.client_combo.addItem("Client")
        asset_task_layout = make_row("Asset", "asset_combo", "Task", "task_combo")

        self.selector_frame.content_layout().addLayout(client_project_layout)
        self.selector_frame.content_layout().addLayout(asset_task_layout)

        combo_dict = {
            "client": self.client_combo,
            "project": self.project_combo,
            "asset": self.asset_combo,
            "task": self.task_combo
        }

        self.client_combo.currentIndexChanged.connect(lambda: self.on_client_changed(combo_dict))
        self.project_combo.currentIndexChanged.connect(lambda: self.on_project_changed(combo_dict))
        self.asset_combo.currentIndexChanged.connect(lambda: self.on_asset_changed(combo_dict))
        self.task_combo.currentIndexChanged.connect(lambda: self.on_task_changed(combo_dict))

        logic_selector.setup_context_menu(self.client_combo, "client")
        logic_selector.setup_context_menu(self.project_combo, "project")
        logic_selector.setup_context_menu(self.asset_combo, "asset")
        logic_selector.setup_context_menu(self.task_combo, "task")

    def create_folder_content_list_section(self):
        self.folder_content_frame = custom_frame.Frame(name="Section")

        self.folder_content_list = QtWidgets.QTreeWidget()
        self.folder_content_list.setItemDelegate(rid.RoundedItemDelegate(self.folder_content_list))
        self.folder_content_list.setObjectName("AssetList")
        self.folder_content_list.setColumnCount(2)
        self.folder_content_list.setHeaderHidden(True)
        self.folder_content_list.setIndentation(0)
        self.folder_content_list.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.folder_content_frame.content_layout().addWidget(self.folder_content_list)

        self.folder_content_list.itemDoubleClicked.connect(
            lambda item, column: logic_folder_content.open_file(self, item, column, self.recent_files_tree)
        )

        logic_folder_content.setup_files_context_menu(self.folder_content_list)

    def create_recent_files_section(self):
        self.recent_files_tree = QtWidgets.QTreeWidget()
        self.recent_files_tree.setItemDelegate(rid.RoundedItemDelegate(self.recent_files_tree))
        self.recent_files_tree.setObjectName("AssetList")
        self.recent_files_tree.setHeaderHidden(True)
        self.recent_files_tree.setIndentation(0)

        self.recent_files_layout = QtWidgets.QVBoxLayout()
        self.recent_files_layout.addWidget(self.recent_files_tree)

        self.recent_files_tree.itemClicked.connect(
            lambda item, column: logic_folder_content.on_recent_file_clicked(self, item, column)
        )

        logic_folder_content.refresh_recent_files(self.recent_files_tree)
        logic_folder_content.setup_recent_context_menu(self.recent_files_tree)

    def create_bottom_section_tabs(self):
        self.create_recent_files_section()

        recent_files_tab = QtWidgets.QWidget()
        recent_files_tab.setLayout(self.recent_files_layout)

        client_io_tab = QtWidgets.QWidget()
        # client_io_tab.setLayout(self.folder_hierarchy_layout)

        maya_tab = QtWidgets.QWidget()

        self.tabs_widget = QtWidgets.QTabWidget()
        self.tabs_widget.addTab(recent_files_tab, "Recent Files")
        self.tabs_widget.addTab(client_io_tab, "Client IO")
        self.tabs_widget.addTab(maya_tab, "Maya Folder")

        self.recent_files_frame = custom_frame.Frame(name="Section", fixed_height=250)
        self.recent_files_frame.content_layout().addWidget(self.tabs_widget)

    # SIGNALS
    def on_client_changed(self, combo_dict: dict[QtWidgets.QComboBox]):
        current_env = {
            "client": self.client_combo.currentText(),
            "project": "",
            "asset": "",
            "task": ""
        }
        logic_selector.update_comboboxes_from_fs(self, "client", current_env, combo_dict)

    def on_project_changed(self, combo_dict: dict[QtWidgets.QComboBox]):
        current_env = {
            "client": self.client_combo.currentText(),
            "project": self.project_combo.currentText(),
            "asset": "",
            "task": ""
        }

        logic_selector.update_comboboxes_from_fs(self, "project", current_env, combo_dict)

    def on_asset_changed(self, combo_dict: dict[QtWidgets.QComboBox]):

        current_env = {
            "client": self.client_combo.currentText(),
            "project": self.project_combo.currentText(),
            "asset": self.asset_combo.currentText(),
            "task": ""
        }

        logic_selector.update_comboboxes_from_fs(self, "asset", current_env, combo_dict)

    def on_task_changed(self, combo_dict: dict[QtWidgets.QComboBox]):
        current_env = {
            "client": self.client_combo.currentText(),
            "project": self.project_combo.currentText(),
            "asset": self.asset_combo.currentText(),
            "task": self.task_combo.currentText()
        }

        logic_selector.update_comboboxes_from_fs(self, "task", current_env, combo_dict)
