import os
import json
import time
import subprocess
import platform

from maya import cmds

from BetterFileExplorer.config import settings

current_os = platform.system().lower()


def build_tree(path):
    """
    path = "D:/Users/OneDrive/Documents/Projects/BetterFileExplorer/TemplateClient"
    output = f"{settings.ROOT_DIR}/config/data/hierarchy_profiles/short.json"
    result = build_tree(path)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Structure créée dans : {output}")
    """
    name = os.path.basename(os.path.normpath(path))
    tree = {
        "name": name,
        "children": []
    }

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return [tree]

    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            subtree = build_tree(full_path)[0]
            tree["children"].append(subtree)

    return [tree]


def create_folders_from_tree(data, parent_path):
    """
    json_path = f"{settings.ROOT_DIR}/config/data/hierarchy_profiles/extended.json"
    output_root = "D:/Users/OneDrive/Documents/Projects/BetterFileExplorer/TemplateClient"

    with open(json_path, "r", encoding="utf-8") as f:
        tree_structure = json.load(f)

    create_folders_from_tree(tree_structure, output_root)

    print(f"Structure créée dans : {output_root}")
    """
    for node in data:
        folder_name = node["name"]
        folder_path = os.path.join(parent_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        children = node.get("children", [])
        if children:
            create_folders_from_tree(children, folder_path)


def get_file_date(file):
    m_time = os.path.getmtime(file)
    date = time.strftime('%m/%d/%Y  | %I:%M %p', time.localtime(m_time))

    return date


def open_containing_folder(path):
    path = os.path.abspath(path)

    if not os.path.exists(path):
        cmds.warning("The file {} does yet exist".format(path))
        return

    if "windows" in current_os:
        if os.path.isdir(path):
            subprocess.Popen(r'explorer "{}"'.format(path))

        elif os.path.isfile(path):
            subprocess.Popen(r'explorer /select,"{}"'.format(path))

    elif "linux" in current_os:
        subprocess.Popen(["xdg-open", os.path.dirname(path)])

    else:
        subprocess.call(["open", "-R", path])


if __name__ == "__main__":
    path = "D:/Users/OneDrive/Documents/Projects/BetterFileExplorer/TemplateClient"
    output = f"{settings.ROOT_DIR}/config/data/hierarchy_profiles/short.json"
    result = build_tree(path)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Structure créée dans : {output}")
