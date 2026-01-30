## 게임 기록 관련 입출력 모듈입니다.

from pydantic import BaseModel

class GamesResponse(BaseModel):
    record_id: int
    category: str
    played_at: str
    gain_point: int

    class Config:
        from_attributes = True