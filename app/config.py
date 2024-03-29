from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # database settings
    db_hostname: str
    db_port: int
    db_username: str
    db_password: str
    db_name: str

    # OAuth2 settings
    secret_key: str
    algorithm: str
    token_expire_minutes: int

    class Config:
        env_file = 'env.env'


settings = Settings()
