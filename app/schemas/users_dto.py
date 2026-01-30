## 사용자 관련 입출력 모듈입니다.

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 응답 데이터
class UserResponse(BaseModel):
    user_id: str
    name: str
    profile_image: Optional[str] = None
    current_point: int
    region: Optional[str] = None
    created_at: Optional[datetime] = None