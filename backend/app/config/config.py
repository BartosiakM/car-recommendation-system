import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"



settings = Settings(
    database_url=os.getenv("DATABASE_URL", "sqlite:///./dev.db"),
    secret_key=os.getenv("SECRET_KEY", "dev_secret_change_me"),
)
