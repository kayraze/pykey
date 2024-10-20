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

