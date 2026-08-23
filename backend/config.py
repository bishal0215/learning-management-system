from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key:str
    algorithm: str
    access_token_expire_minutes:int
    refresh_token_expire_days: int = 7
    database_url:str

    class Config:
        env_file =".env"

settings = Settings() 