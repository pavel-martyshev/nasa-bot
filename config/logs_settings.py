from dataclasses import dataclass


@dataclass
class LogsSettings:
    """
    Settings for the logging configuration.

    Attributes:
        level: Logging level (e.g., DEBUG, INFO, WARNING).
        dir_name: Directory name where log files will be stored.
        file_name: Name of the log file.
        handlers_format: Format string for log entries.
        date_format: Format string for dates in logs.
        time_rotating: Interval type for rotating logs (e.g., 'midnight', 'H' for hourly).
        backup_count: Number of backup log files to keep.
    """
    level: str
    dir_name: str
    file_name: str

    handlers_format: str
    date_format: str

    time_rotating: str
    backup_count: int
