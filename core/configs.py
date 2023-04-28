from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'mysql+asyncmy://root:root@localhost:3306/faculdade?charset=utf8mb4'

    class Config:
        case_sensitive = True

settings: Settings = Settings()