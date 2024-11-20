from scraper import RecordScraper
from interface import Interface
from config import create_records_folder

def main():
    scraper = RecordScraper()
    interface = Interface(scraper)
    create_records_folder()
    interface.mainloop()

if __name__ == "__main__":
    main()
