from dataclasses import dataclass


@dataclass
class DatabaseSettings:
    """
    Holds connection settings for Redis and Postgres databases.

    Attributes:
        redis_host (str): Redis host name.
        redis_port (int): Redis port.
        redis_db_number (int): Redis database number.

        postgres_host (str): Postgres host name.
        postgres_port (int): Postgres port.
        postgres_user (str): Postgres username.
        postgres_password (str): Postgres password.
        postgres_db_name (str): Name of the Postgres database.
    """

    redis_host: str
    redis_port: int
    redis_db_number: int

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db_name: str
