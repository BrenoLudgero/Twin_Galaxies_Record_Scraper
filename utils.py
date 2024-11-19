from pandas import ExcelWriter

def sanitize_category_name(category_name):
    """
    Removes invalid characters from the category name and 
    limits its length to comply with Excel's sheet name format
    """
    return category_name.translate(str.maketrans("[]/:", "()|>"))[:31]

def save_to_excel(records, file_name, output_directory):
    """
    Saves records to an Excel file with separate sheets for each category
    """
    file_path = f"{output_directory}/{file_name}.xlsx"
    with ExcelWriter(file_path, engine="openpyxl") as writer:
        for category_name, data in records.items():
            data.to_excel(writer, sheet_name=category_name, index=False)
