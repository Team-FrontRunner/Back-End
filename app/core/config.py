import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

    # [추가] Solar (Upstage) API Key
    SOLAR_API_KEY: str = os.getenv("SOLAR_API_KEY")
    SOLAR_BASE_URL: str = "https://api.upstage.ai/v1/solar"  # Solar 기본 엔드포인트


settings = Settings()