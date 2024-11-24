import sys
from pathlib import Path
from pandas import ExcelWriter
from config.setup import RECORDS_FOLDER_NAME

def is_running_from_executable():
    return getattr(sys, "frozen", False)

def get_root_directory():
    if is_running_from_executable():
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent.parent

def get_records_folder_path():
    root_dir = get_root_directory()
    return root_dir / RECORDS_FOLDER_NAME

def create_records_folder_if_missing():
    records_folder = get_records_folder_path()
    if not records_folder.is_dir():
        records_folder.mkdir(parents=True, exist_ok=True)

def export_data_to_excel(data, file_name):
    create_records_folder_if_missing()
    file_path = f"{get_records_folder_path()}/{file_name}.xlsx"
    with ExcelWriter(file_path, engine="openpyxl") as writer:
       for category_name, data in data.items():
           data.to_excel(writer, sheet_name=category_name, index=False)
