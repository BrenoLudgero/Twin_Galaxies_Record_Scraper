from scraper import RecordScraper
from interface import Interface

def main():
    scraper = RecordScraper()
    interface = Interface(scraper)
    interface.mainloop()

if __name__ == "__main__":
    main()
