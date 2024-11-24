def sanitize_category_name(category_name):
    return category_name.translate(str.maketrans("[]/:", "()|>"))[:31]

def ensure_proper_url(url, main_url):
    url = url.lower()
    if "twingalaxies.com" not in url:
        return f"{main_url}{url}"
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url

def get_formatted_file_name_from_url(url):
    url = url + "/" if not url.endswith("/") else url
    shortened_url = url.split("game/")[1]
    parts = [part for part in shortened_url.split("/") if part]
    result = parts[0:3] if len(parts) > 3 else parts
    return "_".join(result)
