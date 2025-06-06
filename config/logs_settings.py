from dataclasses import dataclass


@dataclass
class LogsSettings:
    """
    Configuration settings for application logging.

    Attributes:
        level (str): Logging level (e.g., "DEBUG", "INFO").
        dir_name (str): Directory where log files are stored.
        file_name (str): Log file name.
        handlers_format (str): Format string for log messages.
        date_format (str): Format string for timestamps in logs.
        time_rotating (str): Rotation interval (e.g., "midnight", "H" for hourly).
        backup_count (int): Number of rotated log files to retain.
    """

    level: str
    dir_name: str
    file_name: str

    handlers_format: str
    date_format: str

    time_rotating: str
    backup_count: int
