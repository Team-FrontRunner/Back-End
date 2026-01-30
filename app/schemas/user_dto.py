## 사용자 관련 입출력 모듈입니다.

from pydantic import BaseModel
from typing import Optional

# 회원가입 시 받을 데이터
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

# 응답으로 보낼 데이터 (비밀번호 제외 등)
class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str] = None