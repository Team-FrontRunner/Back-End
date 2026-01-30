## 건강 기록 관련 입출력 모듈입니다.

from pydantic import BaseModel
from typing import Optional

# [기존] GET 응답용 (유지)
class HealthResponse(BaseModel):
    record_id: int
    content: Optional[str] = None
    category: str
    created_at: str

    class Config:
        from_attributes = True

# [신규] POST 요청용 (사용자 말 내용)
class HealthRecordRequest(BaseModel):
    content: str

# [신규] POST 응답용 (저장 결과 및 자동 분류된 카테고리)
class HealthRecordPostResponse(BaseModel):
    record_id: int
    assigned_category: str
    created_at: str