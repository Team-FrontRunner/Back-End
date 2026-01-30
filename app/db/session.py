## Supabase 클라이언트를 생성하는 모듈입니다.

from supabase import create_client, Client
from app.core.config import settings

# URL이나 키가 없으면 에러를 띄워주는 안전장치
if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
    raise ValueError("Supabase 환경변수가 설정되지 않았습니다.")

# 전역에서 사용할 Supabase 클라이언트 객체
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)