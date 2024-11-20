from pandas import ExcelWriter
from config import get_records_folder_path

# Removes invalid characters from the category name and 
# limits its length to comply with Excel's sheet name format
def sanitize_category_name(category_name):
    return category_name.translate(str.maketrans("[]/:", "()|>"))[:31]

def ensure_proper_url(url, main_url):
    url = url.lower()
    if "twingalaxies.com" not in url:
        return f"{main_url}{url}"
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url

# Extracts the the name, platform, and category
# present in the url and separates them with a "_"
def get_formatted_file_name_from_url(url):
    url = url + "/" if not url.endswith("/") else url
    shortened_url = url.split("game/")[1]
    parts = [part for part in shortened_url.split("/") if part]
    result = parts[0:3] if len(parts) > 3 else parts
    return "_".join(result)

# Saves records to an Excel file with separate sheets for each category
def save_to_excel(records, file_name):
    file_path = f"{get_records_folder_path()}/{file_name}.xlsx"
    with ExcelWriter(file_path, engine="openpyxl") as writer:
       for category_name, data in records.items():
           data.to_excel(writer, sheet_name=category_name, index=False)
