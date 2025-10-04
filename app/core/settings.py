from urllib.parse import quote_plus

from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    TELEGRAM_BOT_TOKEN: str = '7508451034:AAFxb7lRCdI-C0C6-WlzAaEQ8vgNi8L80Kw'

    # API Configuration
    API_HOST: str = '0.0.0.0'
    API_PORT: int = 8000
    API_TITLE: str = 'API'
    API_VERSION: str = '1.0.0'
    SHOWING_PERCENTAGE_MATCH: int = 70

    # PostgreSQL Configuration
    PG_HOST: str = 'localhost'
    PG_USER: str = 'vvs'
    PG_PASS: str = '1202'
    PG_PORT: int = 5432
    PG_DB_NAME: str = 'postgres'

    # PostgreSQL Pool Configuration
    PG_POOL_SIZE: int = 5
    PG_MAX_OVERFLOW: int = 10
    PG_POOL_RECYCLE: int = 300
    PG_POOL_PRE_PING: bool = True
    PG_ECHO: bool = False

    # Database Session Configuration
    DB_EXPIRE_ON_COMMIT: bool = False
    DB_AUTOFLUSH: bool = False
    DB_AUTOCOMMIT: bool = False

    @property
    def get_postgres_dsn(self) -> str:
        """Получение строки подключения к PostgreSQL"""
        return (
            f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@'
            f'{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB_NAME}'
        )

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

settings = Settings()