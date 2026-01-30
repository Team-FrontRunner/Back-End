## 사용자 게임 기록 관련 모듈입니다.

from fastapi import APIRouter, HTTPException
from typing import List
from app.db.session import supabase
from app.schemas.games_dto import GamesResponse

router = APIRouter(
    prefix="/game_records",
    tags=["game_records"]
)

@router.get("/", response_model=List[GamesResponse], summary="게임 기록 가져오기")
def get_game_records():
    """
    Supabase 상의 game_records 테이블의 값을 불러와 프론트엔드에 전송합니다.
    """
    try:
        response = supabase.table("game_records").select("*").execute()
        return response.data
    except Exception as e:
        # 실제 운영 환경에서는 로깅을 추가하는 것이 좋습니다.
        raise HTTPException(status_code=500, detail=str(e))