import os

from pathlib import Path

from maya import cmds

from BetterFileExplorer.config import settings
from BetterFileExplorer.core import load
from BetterFileExplorer.core import maya_utils
from BetterFileExplorer.core.python_utils import open_containing_folder

from PySide2 import QtWidgets, QtCore, QtGui


def open_file(main_window, item, column, recent_tree: QtWidgets.QTreeWidget):
    data = item.data(0, QtCore.Qt.UserRole)
    file_path = data["path"]

    if file_path and os.path.exists(file_path):
        if cmds.file(q=True, modified=True):
            confirm = QtWidgets.QMessageBox.question(
                main_window,
                "Unsaved Changes",
                "Current scene has unsaved changes. Continue?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )

            if confirm != QtWidgets.QMessageBox.Yes:
                return

        cmds.file(file_path, open=True, force=True)
    else:
        QtWidgets.QMessageBox.warning(main_window, "File Not Found", f"Cannot find file:\n{file_path}")

    load.save_recent_file(data)
    refresh_recent_files(recent_tree)


def refresh_recent_files(tree: QtWidgets.QTreeWidget):
    tree.clear()
    for recent_data in load.get_recent_files():
        add_recent_file_item(tree, recent_data)


def add_recent_file_item(tree: QtWidgets.QTreeWidget, recent_data):
    path = recent_data["path"]

    item = QtWidgets.QTreeWidgetItem([os.path.basename(path)])
    item.setData(0, QtCore.Qt.UserRole, recent_data)

    tree.addTopLevelItem(item)


def on_recent_file_clicked(main_window, item, column):
    data = item.data(0, QtCore.Qt.UserRole)

    if not isinstance(data, dict):
        return

    main_window.client_combo.setCurrentText(data.get("client", ""))
    main_window.project_combo.setCurrentText(data.get("project", ""))
    main_window.asset_combo.setCurrentText(data.get("asset", ""))
    main_window.task_combo.setCurrentText(data.get("task", ""))

    text = data.get("file_name", "")
    matching_items = main_window.folder_content_list.findItems(text, QtCore.Qt.MatchExactly)
    if matching_items:
        item = matching_items[0]
        main_window.folder_content_list.setCurrentItem(item)


def setup_files_context_menu(tree_widget):
    tree_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    tree_widget.customContextMenuRequested.connect(lambda pos: show_files_context_menu(tree_widget, pos))


def show_files_context_menu(tree_widget, pos):
    item = tree_widget.itemAt(pos)
    if not item:
        return

    menu = QtWidgets.QMenu(tree_widget)

    folder_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/folder_white.png").scaled(14, 14))
    open_action = menu.addAction(folder_icon, "Open In Directory")

    # import_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/import_white.png").scaled(14, 14))
    import_action = menu.addAction("Import File")

    # reference_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/reference_white.svg").scaled(14, 14))
    reference_action = menu.addAction("Reference File")

    global_pos = tree_widget.viewport().mapToGlobal(pos)
    action = menu.exec_(global_pos)

    selected_text = item.text(0)
    if selected_text:
        current_env = load.get_current_environment()
        parent_path = maya_utils.build_path(current_env, "task")
        task = item.data(0, QtCore.Qt.UserRole)["task"]

        file_path = os.path.join(parent_path, task, selected_text)
        filename = Path(file_path).stem
        if action == open_action:
            open_containing_folder(file_path)
        elif action == import_action:
            cmds.file(file_path, i=True)
        elif action == reference_action:
            cmds.file(file_path, reference=True, namespace=filename)


def setup_recent_context_menu(tree_widget):
    tree_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    tree_widget.customContextMenuRequested.connect(lambda pos: show_recent_context_menu(tree_widget, pos))


def show_recent_context_menu(tree_widget, pos):
    item = tree_widget.itemAt(pos)
    if not item:
        return

    menu = QtWidgets.QMenu(tree_widget)

    folder_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/folder_white.png").scaled(14, 14))
    open_action = menu.addAction(folder_icon, "Open In Directory")

    # remove_selected_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/import_white.png").scaled(14, 14))
    remove_selected_action = menu.addAction("Remove Selected")

    # remove_all_icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/reference_white.svg").scaled(14, 14))
    remove_all_action = menu.addAction("Remove All")

    global_pos = tree_widget.viewport().mapToGlobal(pos)
    action = menu.exec_(global_pos)

    selected_text = item.text(0)
    if selected_text:
        current_env = load.get_current_environment()
        parent_path = maya_utils.build_path(current_env, "task")
        task = item.data(0, QtCore.Qt.UserRole)["task"]

        file_path = os.path.join(parent_path, task, selected_text)

        if action == open_action:
            open_containing_folder(file_path)
        elif action == remove_selected_action:
            json_data = load.get_recent_files()
            remove_selected_entry(tree_widget, json_data)
        elif action == remove_all_action:
            remove_all_entries(tree_widget)


def remove_selected_entry(tree_widget, json_data):
    current_item = tree_widget.currentItem()
    current_selection = tree_widget.selectedItems()
    print(current_item)
    print(current_selection)
    for sel in current_selection:
        entry = sel.data(0, QtCore.Qt.UserRole)
        if not entry:
            return

        path_to_remove = entry.get("path")
        if not path_to_remove:
            return

        new_recent_data = [item for item in json_data if item.get("path") != path_to_remove]
        load.save_json(settings.RECENT_FILE_PATH, new_recent_data)

        index = tree_widget.indexOfTopLevelItem(sel)
        tree_widget.takeTopLevelItem(index)


def remove_all_entries(tree_widget):
    load.save_json(settings.RECENT_FILE_PATH, [])
    tree_widget.clear()
