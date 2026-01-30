## 사용자 건강 및 모닝콜 기록 관련 모듈입니다.

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.db.session import supabase
from app.schemas.health_dto import HealthResponse, HealthRecordRequest, HealthRecordPostResponse

router = APIRouter(
    prefix="/records/health",
    tags=["health_records"]
)

# --- [Helper] 간단한 카테고리 분류 함수 ---
def predict_category(content: str) -> str:
    """
    내용(content)에 포함된 키워드를 기반으로 카테고리를 추정합니다.
    (추후 AI 모델로 고도화 가능)
    """
    content = content.replace(" ", "") # 공백 제거 후 검사
    if any(word in content for word in ["아파", "쑤시", "통증", "약", "병원", "허리", "무릎", "머리"]):
        return "통증"
    elif any(word in content for word in ["먹", "맛있", "밥", "식사", "배불", "반찬", "입맛"]):
        return "식사"
    elif any(word in content for word in ["좋", "행복", "즐거", "우울", "슬퍼", "화나", "짜증"]):
        return "기분"
    elif any(word in content for word in ["잠", "졸려", "일어", "꿈", "자고"]):
        return "수면"
    else:
        return "일상"

# --- [기존] 조회 API ---
@router.get("/{user_id}", response_model=List[HealthResponse], summary="특정 사용자 건강/모닝콜 기록 조회")
def get_user_health_records(user_id: str, category: Optional[str] = Query(None)):
    try:
        query = supabase.table("health_records").select("*").eq("user_id", user_id)
        if category:
            query = query.eq("category", category)
        response = query.order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- [신규] 저장 API (POST) ---
@router.post("/{user_id}", response_model=HealthRecordPostResponse, summary="건강 기록 저장 (카테고리 자동분류)")
def create_health_record(user_id: str, request: HealthRecordRequest):
    """
    [POST] /api/records/health/{user_id}
    * content: 음성 인식된 텍스트
    * 기능: 텍스트를 분석해 카테고리를 자동 분류("식사", "통증" 등)하여 저장합니다.
    """
    try:
        # 1. 카테고리 자동 분류
        assigned_category = predict_category(request.content)

        # 2. DB 저장 데이터 준비
        data = {
            "user_id": user_id,
            "content": request.content,
            "category": assigned_category
            # created_at은 DB에서 자동 생성됨
        }

        # 3. Supabase Insert
        response = supabase.table("health_records").insert(data).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="기록 저장 실패")

        # 4. 결과 반환
        new_record = response.data[0]
        return {
            "record_id": new_record['record_id'],
            "assigned_category": new_record['category'], # DB에 저장된 카테고리 반환
            "created_at": new_record['created_at']
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))