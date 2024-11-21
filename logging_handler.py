import logging

class TextboxLogHandler(logging.Handler):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox

    def emit(self, record):
        log_message = self.format(record) + "\n"
        self.textbox.configure(state="normal")
        self.textbox.insert("end", log_message)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def configure_logging(self):
        self.setLevel(logging.INFO)
        log_formatter = logging.Formatter("%(asctime)s %(levelname)s:  %(message)s", "%H:%M:%S")
        self.setFormatter(log_formatter)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(self)
