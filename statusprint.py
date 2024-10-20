import cprint


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