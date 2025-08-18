import os

from maya import cmds

from BetterFileExplorer.config import settings
from BetterFileExplorer.core import load
from BetterFileExplorer.core import maya_utils
from BetterFileExplorer.core.python_utils import get_file_date, open_containing_folder

from PySide2 import QtWidgets, QtCore, QtGui


def create_client_hierarchy_from_template(window: QtWidgets.QDialog,
                                          role: str,
                                          line_edit_widget: QtWidgets.QLineEdit,
                                          main_window: QtWidgets.QDialog):
    """
    Create folder hierarchy from a structured list of dictionaries when client is created.
    """
    data = load.get_hierarchy_template_list()
    current_env = load.get_current_environment()
    user_input = line_edit_widget.text()

    if not user_input:
        cmds.warning("Please input a name.")
        return

    full_path = maya_utils.build_path(current_env, role)

    if role == "client":
        if not os.path.exists(os.path.join(full_path, user_input)):
            recurse_on_folders(data, full_path, user_input, role)
            load.update_selector_black_list(data)
        else:
            cmds.warning(f"Client folder '{user_input}' already exists.")
    else:
        check_template_folder_exist(data, full_path, user_input, role)

    current_env[role] = user_input
    load.save_current_environment(current_env)

    window.close()
    update_selector_on_env(main_window, current_env)


def recurse_on_folders(data, path, user_input=None, role=None):
    """Recursively create folders from nested JSON structure."""
    for item in data:
        folder_name = item.get("name")

        if not folder_name:
            continue
        if item.get("role") == role:
            folder_name = user_input

        current_path = os.path.join(path, folder_name)
        os.makedirs(current_path, exist_ok=True)

        children = item.get("children", [])
        if children:
            recurse_on_folders(children, current_path, user_input, role)


def check_template_folder_exist(data, path, user_input, role):
    file_name_check = f"{role.upper()} NAME"
    original = os.path.join(path, file_name_check)
    destination = os.path.join(path, user_input)

    if os.path.exists(original):
        if not os.path.exists(destination):
            os.rename(original, destination)
        else:
            cmds.warning(f"Target folder '{user_input}' already exists.")
            return
    else:
        role_branch = find_branch_by_role(data, role)
        recurse_on_folders([role_branch], path, user_input, role)


def find_branch_by_role(data, role):
    for item in data:
        if item.get("role") == role:
            return item
        children = item.get("children", [])
        if children:
            result = find_branch_by_role(children, role)
            if result:
                return result
    return None


def update_selector_on_env(main_window: QtWidgets.QDialog, current_env: dict) -> None:
    client_items = get_items(current_env, "client")
    project_items = get_items(current_env, "project")
    asset_items = get_items(current_env, "asset")
    task_items = get_items(current_env, "task")

    populate_combobox(main_window.client_combo, current_env, client_items, "client")
    if project_items:
        populate_combobox(main_window.project_combo, current_env, project_items, "project")
    else:
        main_window.project_combo.clear()
    if asset_items:
        populate_combobox(main_window.asset_combo, current_env, asset_items, "asset")
    else:
        main_window.asset_combo.clear()
    if task_items:
        populate_combobox(main_window.task_combo, current_env, task_items, "task")
    else:
        main_window.task_combo.clear()


def get_items(current_env, role):
    items_path = maya_utils.build_path(current_env, role)

    if os.path.exists(items_path):
        black_list = load.open_json(f"{settings.DATA_PATH}/selector_word_black_list.json")
        return [item for item in os.listdir(items_path) if item not in black_list]
    else:
        return None


def populate_combobox(combobox, current_env, items, role):
    combobox.clear()
    combobox.addItems(items)

    if current_env:
        new_value = current_env.get(role, None)
        if new_value:
            combobox.setCurrentText(new_value)


def update_comboboxes_from_fs(main_window: QtWidgets.QDialog,
                              role: str,
                              current_env: dict,
                              combo_dict: dict[str, QtWidgets.QComboBox]):
    """
    Dynamically updates the combo boxes based on the existing folders.

    :param main_window: Main window object.
    :param role: 'client', 'project' or 'asset' (the role that was changed).
    :param current_env: Dictionary representing the current environment.
    :param combo_dict: Dictionary containing the QComboBoxes {'client': ..., 'project': ..., 'asset': ..., 'task': ...}
    :param default_task: Optional string representing the default task to select.
    """

    def _update_field(field: str):
        # Update a single combo box and the corresponding value in current_env.
        items = get_items(current_env, field) or []
        combo = combo_dict.get(field)

        combo.blockSignals(True)
        combo.clear()
        combo.addItems(items)

        if field == "task":
            default_task = load.get_default_task()
            if default_task and default_task in items:
                combo.setCurrentText(default_task)

        combo.blockSignals(False)

        current_env[field] = combo.currentText() if items else ""

    # Define which fields to update for each role
    role_to_fields = {
        "client": ["project", "asset", "task"],
        "project": ["asset", "task"],
        "asset": ["task"]
    }

    for roles in role_to_fields.get(role, []):
        _update_field(roles)

    load.save_current_environment(current_env)

    is_task = combo_dict["task"].currentText()
    if is_task:
        display_assets(main_window, current_env)


def display_assets(main_window: QtWidgets.QDialog, current_env: dict):
    tasks_path = maya_utils.build_path(current_env, "task")
    assets_path = os.path.join(tasks_path, current_env["task"])

    asset_files = [i for i in os.listdir(assets_path) if not i.startswith(".")]
    main_window.folder_content_list.clear()

    for asset in asset_files:
        full_asset_path = os.path.join(assets_path, asset)
        date = get_file_date(full_asset_path)
        item = QtWidgets.QTreeWidgetItem([asset, date])
        item.setData(0, QtCore.Qt.UserRole, {
            "path": full_asset_path,
            "file_name": asset,
            "client": current_env["client"],
            "project": current_env["project"],
            "asset": current_env["asset"],
            "task": current_env["task"]
        })
        item.setTextAlignment(1, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        main_window.folder_content_list.addTopLevelItem(item)


def setup_context_menu(widget, name):
    widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    widget.customContextMenuRequested.connect(lambda pos, w=widget, n=name: show_context_menu(w, n))


def show_context_menu(combo, name):
    menu = QtWidgets.QMenu(combo)

    icon = QtGui.QIcon(QtGui.QPixmap(f"{settings.ROOT_DIR}/resources/icons/folder_white.png").scaled(14, 14))
    open_action = menu.addAction(icon, f"Open In Directory")
    action = menu.exec_(combo.mapToGlobal(QtCore.QPoint(0, combo.height())))

    if action == open_action:
        selected_text = combo.currentText()
        if selected_text:
            current_env = load.get_current_environment()
            parent_path = maya_utils.build_path(current_env, name)

            open_containing_folder(parent_path)
