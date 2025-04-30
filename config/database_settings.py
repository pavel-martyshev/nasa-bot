from dataclasses import dataclass


@dataclass
class DatabaseSettings:
    """
    Settings for database configurations (e.g., Postgres).

    Attributes:
        redis_host: Redis host name.
        redis_port: Redis port.
        redis_db_number: Redis database number.

        postgres_host: Postgres host name.
        postgres_port: Postgres port.
        postgres_user: Postgres username.
        postgres_password: <PASSWORD>.
    """
    redis_host: str
    redis_port: int
    redis_db_number: int

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db_name: str
