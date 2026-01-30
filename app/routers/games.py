## 사용자 게임 기록 관련 모듈입니다.

from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.db.session import supabase
from app.schemas.games_dto import GamesResponse, GameRecordRequest, GameRecordPostResponse

router = APIRouter(
    prefix="/records/game",
    tags=["game_records"]
)


# --- [기존] 모든 기록 가져오기 (관리자용 등으로 사용 가능) ---
@router.get("/", response_model=List[GamesResponse], summary="전체 게임 기록 가져오기")
def get_game_records():
    try:
        response = supabase.table("game_records").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- [신규] 특정 유저의 기록 가져오기 (GET) ---
@router.get("/{user_id}", response_model=List[GamesResponse], summary="특정 유저 게임 기록 조회")
def get_user_game_records(user_id: str, limit: int = 10):
    """
    [GET] /api/records/game/{user_id}?limit=10
    * user_id: 조회할 사용자 ID
    * limit: 가져올 기록 개수 (기본값 10)
    """
    try:
        # 1. game_records 테이블에서 user_id가 일치하는 것 선택
        # 2. order("played_at", desc=True): 최신순 정렬 (최근 게임이 위로)
        # 3. limit(limit): 요청받은 개수만큼만 자름
        response = supabase.table("game_records") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("played_at", desc=True) \
            .limit(limit) \
            .execute()

        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- [기존] 게임 기록 저장하기 (POST) ---
@router.post("/{user_id}", response_model=GameRecordPostResponse, summary="게임 기록 저장 및 포인트 적립")
def create_game_record(user_id: str, request: GameRecordRequest):
    try:
        # 1. 유저 포인트 조회
        user_res = supabase.table("users").select("current_point").eq("user_id", user_id).execute()
        if not user_res.data:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        current_point = user_res.data[0]['current_point']
        new_point = current_point + request.gain_point

        # 2. 포인트 업데이트
        supabase.table("users").update({"current_point": new_point}).eq("user_id", user_id).execute()

        # 3. 기록 저장
        record_data = {
            "user_id": user_id,
            "category": request.category,
            "gain_point": request.gain_point,
            # played_at은 DB Default 값 사용
        }
        insert_res = supabase.table("game_records").insert(record_data).execute()

        if not insert_res.data:
            raise HTTPException(status_code=500, detail="기록 저장 실패")

        return {
            "record_id": insert_res.data[0]['record_id'],
            "updated_point": new_point,
            "message": "적립완료."
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))