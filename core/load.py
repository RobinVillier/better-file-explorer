import os
import re
import json

from BetterFileExplorer.config import settings


def load_qss_with_fixed_urls(qss_path):
    base_dir = os.path.dirname(qss_path)

    qss = load_stylesheet(qss_path)

    def replace_url(match):
        relative_path = match.group(1).strip('\'"')
        absolute_path = os.path.abspath(os.path.join(base_dir, relative_path))

        qt_path = absolute_path.replace("\\", "/")
        return f"url({qt_path})"

    fixed_qss = re.sub(r'url\(([^)]+)\)', replace_url, qss)
    return fixed_qss


def load_stylesheet(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def open_json(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as jsonfile:
            jsondata = ''.join(line for line in jsonfile if not line.startswith('//'))
            data = json.loads(jsondata)
            return data
    return {}


def save_json(file_path, content):
    with open(file_path, 'w') as f:
        json.dump(content, f, indent=4)


def get_settings() -> dict:
    return open_json(settings.SETTINGS_PATH)


def save_settings_parameter(key, value):
    settings_dict = get_settings()
    settings_dict[key] = value
    save_json(settings.SETTINGS_PATH, settings_dict)


def get_project_path() -> str:
    return get_settings()["project_path"]


def get_hierarchy_template_list():
    current_profile = settings.get_current_hierarchy_profile()
    return open_json(f"{settings.DATA_PATH}/hierarchy_profiles/{current_profile}.json")


def get_default_task() -> str:
    return open_json(settings.SETTINGS_PATH)["default_task"]


def get_current_environment() -> dict:
    return open_json(f"{settings.SETTINGS_PATH}")["current_environment"]


def save_current_environment(environment_dict: dict) -> None:
    save_settings_parameter("current_environment", environment_dict)


def collect_names(data):
    names = []

    def recurse(items):
        for item in items:
            name = item.get("name")
            if name:
                names.append(name)
                if name == "maya":
                    continue
            if name != "maya" and "children" in item:
                recurse(item["children"])

    recurse(data)
    return names


def update_selector_black_list(data):
    black_list = collect_names(data)
    save_json(f"{settings.DATA_PATH}/selector_word_black_list.json", black_list)


def get_recent_files():
    if os.path.exists(settings.RECENT_FILE_PATH):
        return open_json(settings.RECENT_FILE_PATH)
    return []


def save_recent_file(data_dict):
    recent = get_recent_files()

    recent = [f for f in recent if f["path"] != data_dict["path"]]
    recent.insert(0, data_dict)

    recent_files_amount = open_json(settings.SETTINGS_PATH)["recent_files_amount"]
    recent = recent[:int(recent_files_amount)]

    save_json(settings.RECENT_FILE_PATH, recent)
