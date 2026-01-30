## 환경변수를 로딩하고 설정을 관리하는 모듈입니다.

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    
    # JWT 설정 (개발용 비밀키, 배포 시엔 .env로 이동 권장)
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev_secret_key_1234")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1일

settings = Settings()