import os
import shutil

from maya import cmds

from BetterFileExplorer.core import load
from BetterFileExplorer.core import maya_utils

from PySide2 import QtWidgets


def update_environment(window: QtWidgets.QDialog):
    current_env = load.get_current_environment()
    path = maya_utils.build_path(current_env, current_env.get("task", "task"))

    text = (f"<a href='{path}'>{current_env.get('client', '')} | "
            f"{current_env.get('project', '')} | "
            f"{current_env.get('asset', '')} | "
            f"{current_env.get('task', '')}</a>")

    window.current_env_label.setText(text)

    try:
        window.current_env_label.linkActivated.disconnect()
    except (RuntimeError, TypeError):
        pass

    window.current_env_label.linkActivated.connect(lambda: os.startfile(path))


def update_file_name_preview(window: QtWidgets.QDialog):
    file_name_preview = build_name_from_environment(window)
    window.file_name_preview_label.setText(file_name_preview)


def save_file(window: QtWidgets.QDialog):
    current_env = load.get_current_environment()
    path = maya_utils.build_path(current_env, current_env.get("task", "task"))

    file_name = build_name_from_environment(window)

    if cmds.file(query=True, sceneName=True):
        cmds.file(save=True, type="mayaAscii", f=True)

    if window.publish_rb.isChecked():
        create_next_version_on_publish(current_env, path)

    new_file = os.path.join(path, file_name)
    cmds.file(rename=new_file)
    cmds.file(save=True, type="mayaAscii", f=True)

    add_to_recent_files(new_file)


def build_name_from_environment(window: QtWidgets.QDialog):
    current_env = load.get_current_environment()

    current_version, sub_version = get_versions(window, current_env)
    file_name = f"{current_env['asset']}_{current_env['task']}_v{current_version}.{sub_version}.ma"

    return file_name


def get_versions(window: QtWidgets.QDialog, current_env) -> list:
    path = maya_utils.build_path(current_env, current_env.get("task", "task"))

    items_list = os.listdir(path)
    if items_list:
        item_split = items_list[-1].split(".")
        version = f"{int(item_split[0][-3:]):03d}"

        if window.publish_rb.isChecked():
            sub_version = "pub"
        else:
            sub_version = f"{int(item_split[-2])+1:03d}"

        return [version, sub_version]
    else:
        return ["001", "001"]


def create_next_version_on_publish(current_env, path):
    last_item = os.listdir(path)[-1]
    item_split = last_item.split(".")
    version = f"{int(item_split[0][-3:])+1:03d}"
    next_version_item = f"{current_env['asset']}_{current_env['task']}_v{version}.001.ma"

    origin = os.path.join(path, last_item)
    destination = os.path.join(path, next_version_item)
    shutil.copy(origin, destination)


def add_to_recent_files(path):
    data_dict = parse_asset_path(path)
    load.save_recent_file(data_dict)


def parse_asset_path(path):
    norm_path = os.path.normpath(path)
    parts = norm_path.split(os.sep)

    client = parts[parts.index(load.get_project_file_name()) + 1]
    project = parts[parts.index(client) + 1]
    asset = parts[parts.index("Assets") + 1]
    task = parts[parts.index("scenes") + 1]

    file_name = os.path.basename(norm_path)

    return {
        "asset": asset,
        "client": client,
        "file_name": file_name,
        "path": norm_path,
        "project": project,
        "task": task
    }
