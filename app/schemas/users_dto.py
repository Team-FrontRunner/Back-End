# app/schemas/users_dto.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 응답 데이터 모델만 남김
class UserResponse(BaseModel):
    user_id: str
    name: str
    profile_image: Optional[str] = None
    current_point: int
    region: Optional[str] = None
    created_at: Optional[datetime] = None