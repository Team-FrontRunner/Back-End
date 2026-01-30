## 사용자 건강 기록 관련 모듈입니다.

from fastapi import APIRouter, HTTPException
from typing import List
from app.db.session import supabase
from app.schemas.health_dto import HealthResponse

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

from fastapi import APIRouter, HTTPException
from typing import List
from app.db.session import supabase
from app.schemas.health_dto import HealthResponse

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
