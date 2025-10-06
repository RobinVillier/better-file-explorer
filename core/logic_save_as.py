import os

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

    cmds.file(rename=os.path.join(path, file_name))
    cmds.file(save=True, type="mayaAscii", f=True)


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
        sub_version = f"{int(item_split[-2]) + 1:03d}"

        if window.publish_rb.isChecked():
            sub_version = "pub"

        return [version, sub_version]
    else:
        return ["001", "001"]
