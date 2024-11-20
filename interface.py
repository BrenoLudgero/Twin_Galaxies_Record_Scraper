import customtkinter as ctk
from config import INSTRUCTIONS

ctk.set_default_color_theme("dark-blue")

class Interface(ctk.CTk):
    def __init__(self, scraper):
        super().__init__()
        self.scraper = scraper
        
        # WINDOW SETUP
        self.window_width = 800
        self.window_height = 600
        self.title("Twin Galaxies Record Scraper")
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

        self.url_list_label = ctk.CTkLabel(self, text="Links List", height=1)
        self.url_list_label.grid(row=0, column=0, columnspan=2, sticky="nwe", pady=(6, 0))

        self.textbox = ctk.CTkTextbox(self, border_width=1, wrap="word")
        self.textbox.insert("1.0", INSTRUCTIONS)
        self.textbox.configure(state="disabled")
        self.textbox.grid(row=0, column=2, sticky="nwes", padx=(3, 10), pady=(10, 0))

        self.button = ctk.CTkButton(self, text="Start", command=self.start_scraping_process)
        self.button.grid(row=1, column=2, sticky="nwes", padx=(3, 10), pady=10)

        self.logs_textbox = ctk.CTkTextbox(self, corner_radius=0, border_width=1, fg_color="lightgray", state="disabled")
        self.logs_textbox.grid(row=2, column=0, columnspan=3, sticky="nwes", padx=10, pady=(0, 10))

    def get_centered_window_coords(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int(((screen_width/2) - (self.window_width/2)) * self._get_window_scaling())
        y = int(((screen_height/2) - (self.window_height/1.9)) * self._get_window_scaling())
        return f"{self.window_width}x{self.window_height}+{x}+{y}"

    def start_scraping_process(self):
        lines = self.url_list_textbox.get("0.0", "end").splitlines()
        urls_to_scrape = [line.replace(" ", "") for line in lines if line.strip()]
        self.scraper.run(urls_to_scrape)
