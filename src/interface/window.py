import customtkinter as ctk
from threading import Thread
from .strings import *
from config.setup import *
from .logger_redirector import LoggerRedirector

ctk.set_default_color_theme(WINDOW_COLOR_THEME)

class Window(ctk.CTk):
    def __init__(self, scraper):
        super().__init__()
        self.scraper = scraper
        
        # WINDOW SETUP
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.title(WINDOW_TITLE)
        self.geometry(self.get_centered_window_coords())
        self.minsize(self.window_width, self.window_height)
        self.columnconfigure((0, 1), weight=6)
        self.columnconfigure(2, weight=4)
        self.rowconfigure(0, weight=6)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=3)

        # ELEMENTS
        self.url_list_textbox = ctk.CTkTextbox(self, corner_radius=4, border_width=2, wrap="word")
        self.url_list_textbox.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nwes", padx=10, pady=(26, 10))

        self.url_list_label = ctk.CTkLabel(self, text=LINKS_LIST_LABEL, height=1)
        self.url_list_label.grid(row=0, column=0, columnspan=2, sticky="nwe", pady=(6, 0))

        self.textbox = ctk.CTkTextbox(self, border_width=1, wrap="word")
        self.textbox.insert("1.0", INSTRUCTIONS)
        self.textbox.configure(state="disabled")
        self.textbox.grid(row=0, column=2, sticky="nwes", padx=(3, 10), pady=(10, 0))

        self.button = ctk.CTkButton(self, text=BUTTON_TEXT, command=self.start_scraping_process)
        self.button.grid(row=1, column=2, sticky="nwes", padx=(3, 10), pady=10)

        self.logs_textbox = ctk.CTkTextbox(self, corner_radius=0, border_width=1, state="disabled")
        self.logs_textbox.grid(row=2, column=0, columnspan=3, sticky="nwes", padx=10, pady=(0, 10))

        self.logs_textbox_label = ctk.CTkLabel(self, text=LOGS_TEXTBOX_LABEL, corner_radius=2, height=25, width=50)
        self.logs_textbox_label.grid(row=2, column=2, columnspan=2, sticky="ne", padx=(0, 13), pady=(3, 0))
        
        # LOGGER REDIRECTOR
        self.logger_redirector = LoggerRedirector(self.logs_textbox)
        self.logger_redirector.configure_logging()

    def get_centered_window_coords(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width/2) - (self.window_width/2)) * self._get_window_scaling())
        y = int(((screen_height/2) - (self.window_height/1.9)) * self._get_window_scaling())
        return f"{self.window_width}x{self.window_height}+{x}+{y}"

    def run_scraper(self, urls_to_scrape):
        self.scraper.scrape_all_games(urls_to_scrape)
        self.after(0, lambda: self.button.configure(state="normal"))

    def start_scraping_process(self):
        self.button.configure(state="disabled")
        url_list_text = self.url_list_textbox.get("0.0", "end").splitlines()
        urls_to_scrape = [line.replace(" ", "") for line in url_list_text if line.strip()]
        Thread(target=self.run_scraper, args=(urls_to_scrape,)).start()
