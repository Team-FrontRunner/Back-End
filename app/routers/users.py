## 사용자 회원가입, 개인 정보 등을 다루는 모듈입니다.

from fastapi import APIRouter, HTTPException
from app.db.session import supabase
from app.schemas.users_dto import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    """모든 유저 조회"""
    response = supabase.table("users").select("*").execute()
    return response.data

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str): # 만약 ID가 UUID라면 int 대신 str로 변경하세요
    """특정 유저 조회 (ID로 검색)"""
    # .eq("컬럼명", 값) -> WHERE user_id = 값
    response = supabase.table("users").select("*").eq("user_id", user_id).execute()

    # 데이터가 비어있으면(유저가 없으면) 404 에러 발생
    if not response.data:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    # Supabase는 리스트 형태([])로 반환하므로 첫 번째 요소([0])를 리턴
    return response.data[0]