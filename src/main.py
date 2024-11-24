# Twin Galaxies Record Scraper
# Copyright © 2024 Breno Ludgero

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from scraping.record_scraper import RecordScraper
from interface.window import Window
from utils.file_handler import create_records_folder_if_missing

def main():
    scraper = RecordScraper()
    interface = Window(scraper)
    create_records_folder_if_missing()
    interface.mainloop()

if __name__ == "__main__":
    main()
