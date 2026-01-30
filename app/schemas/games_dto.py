## 게임 기록 관련 입출력 모듈입니다.

from pydantic import BaseModel
from typing import Optional

# [기존 코드] GET 요청용 (유지)
class GamesResponse(BaseModel):
    record_id: int
    category: str
    played_at: str
    gain_point: int

    class Config:
        from_attributes = True

# [신규 추가] POST 요청용 (Body 데이터)
class GameRecordRequest(BaseModel):
    category: str
    gain_point: int

# [신규 추가] POST 응답용 (완료 메시지 및 업데이트된 포인트)
class GameRecordPostResponse(BaseModel):
    record_id: int
    updated_point: int
    message: str