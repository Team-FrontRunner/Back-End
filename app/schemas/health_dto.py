## 건강 기록 관련 입출력 모듈입니다.

from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    record_id: int
    content: Optional[str] = None
    category: str
    created_at: str

    class Config:
        from_attributes = True