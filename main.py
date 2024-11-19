from config import MAIN_URL, PATHS_TO_SCRAPE, RECORDS_FOLDER_DIRECTORY
from scraper import RecordScraper
from utils import save_to_excel

def main():
    scraper = RecordScraper(MAIN_URL)
    print(f"[INFO] Scraping process initiated. Please wait.")
    for game_path in PATHS_TO_SCRAPE:
        records = scraper.scrape_game_records(game_path)
        if records:
            file_name = game_path.strip("/").replace("/", "_").lower()
            save_to_excel(records, file_name, RECORDS_FOLDER_DIRECTORY)
            print(f"[INFO] Records saved to {RECORDS_FOLDER_DIRECTORY / file_name}")
        else:
            return

if __name__ == "__main__":
    main()
