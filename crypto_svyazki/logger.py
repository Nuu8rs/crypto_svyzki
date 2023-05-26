import logging
import sys
from colorama import Fore, Style, init
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        asctime = self.formatTime(record, self.datefmt)

        prefix = f"{Fore.GREEN}[{asctime}:{levelname}]:{Style.RESET_ALL}"

        if record.levelno == logging.INFO:
            msg_color = Fore.YELLOW
        else:
            msg_color = Fore.RED

        msg = f"{msg_color}{record.getMessage()}{Style.RESET_ALL}"
        return f"{prefix} {msg}"

class Logger_class:
    def __init__(self, filename='log.txt', level=logging.INFO, format='[%(asctime)s: %(levelname)s:] %(message)s', datefmt='%Y-%m-%d | %H:%M'):
        self.logger = logging.getLogger()
        self.logger.setLevel(level)
        file_handler = logging.FileHandler(filename, encoding='utf-8')

        file_formatter = logging.Formatter(format, datefmt)
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.encoding = 'utf-8'

        console_formatter = ColoredFormatter(format, datefmt)
        console_handler.setFormatter(console_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        def handle_uncaught_exceptions(exc_type, exc_value, exc_traceback):
            self.logger.error("Unhandled exception:", exc_info=(exc_type, exc_value, exc_traceback))
            self.logger.shutdown()

        sys.excepthook = handle_uncaught_exceptions
        def thread_except_hook(self, func):
              """
              Декоратор для обработки исключений в потоках.
              """
              def wrapper(*args, **kwargs):
                  try:
                      func(*args, **kwargs)
                  except Exception:
                      self.logger.exception("Необработанное исключение в потоке")

              return wrapper
    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

log = Logger_class()