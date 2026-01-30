## 사용자 관련 입출력 모듈입니다.
import datetime

from pydantic import BaseModel
from typing import Optional

# 프론트엔드에서 보낼 가짜 토큰
class KakaoLoginRequest(BaseModel):
    access_token: str

# 응답 데이터
class UserResponse(BaseModel):
    user_id: str
    name: str
    profile_image_url: str
    current_point: int
    created_at: datetime
    region: str