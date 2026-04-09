from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Тестовое задаени для "ПЭСК"'
    app_description: str = 'Система аутентификации и авторизации - Redis'

    jwt_secret_key: str
    jwt_algorithm: str = 'HS256'
    jwt_access_token_exp: int = 900
    jwt_refresh_token_exp: int = 3600

    redis_host: str = 'localhost'
    redis_port: int = 6379

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)


settings = Settings()
