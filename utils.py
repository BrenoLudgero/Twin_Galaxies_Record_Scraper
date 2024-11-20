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

# Saves records to an Excel file with separate sheets for each category
def save_to_excel(records, file_name, output_directory):
    file_path = f"{output_directory}/{file_name}.xlsx"
    with ExcelWriter(file_path, engine="openpyxl") as writer:
        for category_name, data in records.items():
            data.to_excel(writer, sheet_name=category_name, index=False)
