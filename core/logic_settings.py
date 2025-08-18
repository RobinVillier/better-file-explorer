from pathlib import Path

from maya import cmds

from BetterFileExplorer.config import settings
from BetterFileExplorer.core import load

from PySide2 import QtWidgets, QtGui, QtCore


def get_user_directory(settings_window: QtWidgets.QDialog):
    path = QtWidgets.QFileDialog.getExistingDirectory(settings_window, "Select File")
    if path:
        settings_window.project_path_line_edit.setText(path)


def save_project_path(line_edit):
    path = line_edit.text()
    load.save_settings_parameter("project_path", path)


def update_current_profile(widget: QtWidgets.QComboBox):
    current_profile = widget.currentText()
    load.save_settings_parameter("current_hierarchy_profile", current_profile)


def populate_profile_drop_down(widget: QtWidgets.QComboBox):
    current_profile = settings.get_current_hierarchy_profile()

    widget.clear()
    profiles_list = get_profiles_list()
    widget.addItems(profiles_list)
    widget.setCurrentText(current_profile)


def get_profiles_list():
    dir_path = Path(settings.DATA_PATH) / "hierarchy_profiles"
    return [f.stem for f in dir_path.iterdir() if f.is_file() and f.suffix == ".json" and f.stem[0] != "_"]


def populate_folder_hierarchy_tree(tree_widget: QtWidgets.QTreeWidget):
    tree_widget.clear()
    current_profile = settings.get_current_hierarchy_profile()
    data = load.open_json(f"{settings.DATA_PATH}/hierarchy_profiles/{current_profile}.json")
    folder_icon = QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/folder_white.png")

    list_to_tree(tree_widget.invisibleRootItem(), data, folder_icon)
    tree_widget.expandAll()

    # Updates black list for selector combo boxes
    load.update_selector_black_list(data)


def update_hierarchy_json(tree_widget):
    current_profile = settings.get_current_hierarchy_profile()
    current_profile_path = f"{settings.DATA_PATH}/hierarchy_profiles/{current_profile}.json"

    updated_list = tree_to_list(tree_widget)
    load.save_json(current_profile_path, updated_list)


def list_to_tree(widget: QtWidgets.QTreeWidget, data_list: list, icon: QtGui.QIcon):
    for data in data_list:
        item = QtWidgets.QTreeWidgetItem([data["name"]])
        item.setIcon(0, icon)
        item.setData(0, QtCore.Qt.UserRole, data)

        role = data.get("role")
        if role:
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(f"#ff5a5a")))

        widget.addChild(item)
        if data.get("children"):
            list_to_tree(item, data["children"], icon)


def tree_to_list(tree_widget):
    def recurse(item):
        data = item.data(0, QtCore.Qt.UserRole)

        node = {"name": data.get("name", "")}

        if "role" in data:
            node["role"] = data["role"]

        children = [recurse(item.child(ch)) for ch in range(item.childCount())]

        children.sort(key=lambda x: x["name"].lower())
        node["children"] = children

        return node

    result = []
    for i in range(tree_widget.topLevelItemCount()):
        item = tree_widget.topLevelItem(i)
        result.append(recurse(item))

    return result


def create_default_template(line_edit_widget: QtWidgets.QLineEdit,
                            window: QtWidgets.QDialog):
    new_name = line_edit_widget.text()
    profiles_list = get_profiles_list()

    if new_name in profiles_list:
        cmds.warning("Template name already exist !")
    elif not new_name:
        cmds.warning("Please enter a new name for the template.")
    else:
        default_content = load.open_json(f"{settings.DATA_PATH}/hierarchy_profiles/_default.json")
        load.save_json(file_path=f"{settings.DATA_PATH}/hierarchy_profiles/{new_name}.json",
                       content=default_content)
        window.close()


def create_folder(parent_window: QtWidgets.QDialog, parent_item, tree_widget: QtWidgets.QTreeWidget):
    dialog = QtWidgets.QInputDialog(parent_window)
    dialog.setOption(QtWidgets.QInputDialog.UseListViewForComboBoxItems, False)
    dialog.setWindowTitle("New Folder")
    dialog.setLabelText("Folder name:")

    if dialog.exec_() == QtWidgets.QInputDialog.Accepted:
        folder_name = dialog.textValue()

        parent_data = parent_item.data(0, QtCore.Qt.UserRole)
        new_entry = {"name": folder_name, "children": []}
        parent_data.setdefault("children", []).append(new_entry)

        child_item = QtWidgets.QTreeWidgetItem([folder_name])
        child_item.setData(0, QtCore.Qt.UserRole, new_entry)
        child_item.setIcon(0, QtGui.QIcon(f"{settings.ROOT_DIR}/resources/icons/folder_white.png"))

        parent_item.addChild(child_item)

        if "children" not in parent_data:
            parent_data["children"] = []

        update_hierarchy_json(tree_widget)


def rename_folder(parent_window: QtWidgets.QDialog, item, tree_widget: QtWidgets.QTreeWidget):
    current_name = item.text(0)
    new_name, ok = QtWidgets.QInputDialog.getText(parent_window, "Rename Folder", "New name:", text=current_name)
    if ok and new_name != current_name:
        item.setText(0, new_name)
        item_data = item.data(0, QtCore.Qt.UserRole)

        if isinstance(item_data, dict):
            item_data["name"] = new_name
            item.setData(0, QtCore.Qt.UserRole, item_data)

        update_hierarchy_json(tree_widget)


def delete_folder(parent_window: QtWidgets.QDialog, item, tree_widget: QtWidgets.QTreeWidget):
    parent_item = item.parent()
    if not parent_item:
        QtWidgets.QMessageBox.warning(parent_window, "Warning", "Cannot delete top-level item.")
        return

    reply = QtWidgets.QMessageBox.question(parent_window, "Delete", f"Delete folder '{item.text(0)}'?",
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    if reply == QtWidgets.QMessageBox.Yes:
        parent_data = parent_item.data(0, QtCore.Qt.UserRole)
        item_data = item.data(0, QtCore.Qt.UserRole)
        parent_data["children"].remove(item_data)
        parent_item.removeChild(item)

        update_hierarchy_json(tree_widget)


def get_default_task_list() -> list[str]:
    def recurse(node):
        if isinstance(node, dict):
            if node.get("name") == "scenes":
                return [child["name"] for child in node.get("children", [])]
            for child in node.get("children", []):
                result = recurse(child)
                if result:
                    return result
        elif isinstance(node, list):
            for item in node:
                result = recurse(item)
                if result:
                    return result
        return None

    data = load.get_hierarchy_template_list()
    return recurse(data)


def save_default_task(combo: QtWidgets.QComboBox):
    text = combo.currentText()
    load.save_settings_parameter("default_task", text)


def save_recent_files_amount(spinbox: QtWidgets.QSpinBox):
    count = spinbox.text()
    settings_dict = load.open_json(settings.SETTINGS_PATH)
    settings_dict["recent_files_amount"] = count
    load.save_json(settings.SETTINGS_PATH, settings_dict)


def save_settings(settings_window: QtWidgets.QDialog):
    save_project_path(settings_window.project_path_line_edit)
    save_default_task(settings_window.default_task_combo)
    save_recent_files_amount(settings_window.recent_files_spinbox)
