import logging
import subprocess
import sys
import time

from colorama import Fore, Style
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class LoggingFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        if record.levelno == logging.INFO:
            return f"{Fore.CYAN}{msg}{Style.RESET_ALL}"
        if record.levelno == logging.WARNING:
            return f"{Fore.RED}{msg}{Style.RESET_ALL}"
        return msg


class RestartOnChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = self.start_process()

    def start_process(self):
        return subprocess.Popen(self.command)

    def restart_process(self):
        logging.info("🔁 Code changed. Restarting bot...")
        self.process.kill()
        self.process = self.start_process()

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.restart_process()


if __name__ == "__main__":
    command = [sys.executable, "telegram_bot/__main__.py"]
    event_handler = RestartOnChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path="telegram_bot", recursive=True)
    observer.start()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(LoggingFormatter("%(levelname)s: %(message)s"))
    logger.addHandler(handler)
    logging.warning("👀 Bot reloader started")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
