from PySide2 import QtWidgets
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

from BetterFileExplorer.ui import main_window, settings_window, new_profile_window, new_content_window, save_as_window
from BetterFileExplorer.core import load


def get_maya_main_window() -> QtWidgets.QWidget:
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QMainWindow)


def launch_app():
    if not is_project_path_valid():
        parent = get_maya_main_window()
        settings = settings_window.SettingsUI(parent)

        def on_settings_closed():
            if is_project_path_valid():
                main_ui = main_window.BetterFileExplorerUI(parent)
                main_ui.show()

        settings.finished.connect(on_settings_closed)
        settings.show()
    else:
        parent = get_maya_main_window()
        main = main_window.BetterFileExplorerUI(parent)
        main.show()


def is_project_path_valid():
    project_path = load.get_project_path()
    return bool(project_path)


def launch_settings():
    parent = get_maya_main_window()
    window = settings_window.SettingsUI(parent)
    window.show()


def launch_new_profile():
    parent = get_maya_main_window()
    window = new_profile_window.NewProfileUI(parent)
    window.exec_()


def launch_new_content(role: str, window: QtWidgets.QDialog):
    parent = get_maya_main_window()
    window = new_content_window.NewContentUI(parent, role, window)
    window.exec_()


def launch_save_as():
    parent = get_maya_main_window()
    window = save_as_window.SaveAsUI(parent)
    window.show()
