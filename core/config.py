import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # .env stuff
    SUPABASE_URL: str = "your-project-url"
    SUPABASE_KEY: str = "your-anon-key"
    
    # Engine Settings(can change default symbol from here)
    DEFAULT_SYMBOL: str = "BTC-USD"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
