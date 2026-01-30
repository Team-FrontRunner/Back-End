## 환경변수를 로딩하고 설정을 관리하는 모듈입니다.

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

settings = Settings()