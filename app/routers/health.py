## 사용자 건강 기록 관련 모듈입니다.

from fastapi import APIRouter, HTTPException
from typing import List
from app.db.session import supabase
from app.schemas.health_dto import HealthResponse
from app.utils.ai_analysis import get_health_analysis_result
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("/", response_model=List[HealthResponse], summary="건강 기록 데이터 가져오기")
def get_healths():
    """
    Supabase 상의 health_records 테이블의 값을 불러와 프론트엔드에 전송합니다.
    """
    try:
        response = supabase.table("health_records").select("*").execute()
        return response.data
    except Exception as e:
        # 실제 운영 환경에서는 로깅을 추가하는 것이 좋습니다.
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/{user_id}")
async def analyze_health(user_id: str):
    """
    특정 사용자의 1년치 건강 기록을 조회하여 AI 분석 리포트를 생성합니다.
    """

    # 1. 사용자 이름 가져오기 (프롬프트용)
    user_res = supabase.table("users").select("name").eq("user_id", user_id).execute()
    if not user_res.data:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    user_name = user_res.data[0]["name"]

    # 2. 1년치 데이터 조회 (health_records)
    # 오늘로부터 1년 전 날짜 계산
    one_year_ago = (datetime.now() - timedelta(days=365)).isoformat()

    response = supabase.table("health_records") \
        .select("created_at, category, content") \
        .eq("user_id", user_id) \
        .gte("created_at", one_year_ago) \
        .order("created_at") \
        .execute()

    records = response.data

    # 3. 데이터 유효성 검사
    if not records:
        return {
            "status": "empty",
            "message": "아직 분석할 건강 기록이 없어요. 오늘부터 기록을 시작해보세요!",
            "report": ""
        }

    # 4. [핵심] Utils에 있는 AI 분석 함수 호출
    # 여기서 records(리스트)와 user_name(문자열)을 넘겨줍니다.
    ai_report = await get_health_analysis_result(records, user_name)

    return {
        "status": "success",
        "user_name": user_name,
        "record_count": len(records),
        "report": ai_report  # 마크다운 형태의 긴 텍스트
    }