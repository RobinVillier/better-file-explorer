import webbrowser

from PySide2 import QtWidgets, QtGui

from BetterFileExplorer import main
from BetterFileExplorer.config import settings
from BetterFileExplorer.core import logic_selector


class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super(MenuBar, self).__init__(parent)

        self.parent = parent

        self.create_new_menu()
        self.create_edit_menu()
        self.create_about_menu()

    def create_new_menu(self):
        # Create
        new_menu = self.addMenu("New")

        new_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/new_white.png").scaled(14, 14))

        new_client_action = QtWidgets.QAction(new_icon, "Client", self)
        new_menu.addAction(new_client_action)
        new_client_action.triggered.connect(lambda: main.launch_new_content("client", self.parent))

        new_project_action = QtWidgets.QAction(new_icon, "Project", self)
        new_menu.addAction(new_project_action)
        new_project_action.triggered.connect(lambda: main.launch_new_content("project", self.parent))

        new_asset_action = QtWidgets.QAction(new_icon, "Asset", self)
        new_menu.addAction(new_asset_action)
        new_asset_action.triggered.connect(lambda: main.launch_new_content("asset", self.parent))

    def create_edit_menu(self):
        # Edit
        edit_menu = self.addMenu("Edit")

        settings_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/settings_white.png").scaled(14, 14))
        settings_action = QtWidgets.QAction(settings_icon, "Settings", self)
        edit_menu.addAction(settings_action)
        settings_action.triggered.connect(main.launch_settings)

        save_as_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/save_white_icon.svg").scaled(14, 14))
        save_as_action = QtWidgets.QAction(save_as_icon, "Save As", self)
        edit_menu.addAction(save_as_action)
        save_as_action.triggered.connect(main.launch_save_as)

    def create_about_menu(self):
        # About
        about_menu = self.addMenu("About")

        website_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/profile_white.png").scaled(14, 14))
        bse_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/bse_white.png").scaled(14, 14))

        linkedin_action = QtWidgets.QAction(website_icon, "by Robin Villier", self)
        bse_website_action = QtWidgets.QAction(bse_icon, "with Black Swan Effect", self)

        about_menu.addAction(linkedin_action)
        about_menu.addAction(bse_website_action)

        linkedin_action.triggered.connect(
            lambda: webbrowser.open("https://www.linkedin.com/in/robin-villier/")
        )
        bse_website_action.triggered.connect(
            lambda: webbrowser.open("https://blackswaneffect.com/")
        )
