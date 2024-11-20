from pandas import ExcelWriter

# Removes invalid characters from the category name and 
# limits its length to comply with Excel's sheet name format
def sanitize_category_name(category_name):
    return category_name.translate(str.maketrans("[]/:", "()|>"))[:31]

def ensure_proper_page_link(link, main_url):
    link = link.lower()
    if "twingalaxies.com" not in link:
        return f"{main_url}{link}"
    if not link.startswith(("http://", "https://")):
        return "https://" + link
    return link

# Extracts the the name, platform, and category
# present in the url and separates them with a "_"
def get_formatted_file_name_from_url(url):
    url = url + "/" if not url.endswith("/") else url
    shortened_url = url.split("game/")[1]
    parts = [part for part in shortened_url.split("/") if part]
    result = parts[0:3] if len(parts) > 3 else parts
    return "_".join(result)

# Saves records to an Excel file with separate sheets for each category
def save_to_excel(records, file_name, output_directory):
    file_path = f"{output_directory}/{file_name}.xlsx"
    with ExcelWriter(file_path, engine="openpyxl") as writer:
        for category_name, data in records.items():
            data.to_excel(writer, sheet_name=category_name, index=False)
