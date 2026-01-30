## 사용자 회원가입, 개인 정보 등을 다루는 모듈입니다.

from fastapi import APIRouter, HTTPException, Depends
from app.db.session import supabase
from app.schemas.users_dto import UserResponse
from app.core.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, current_user = Depends(get_current_user)): 
    """
    특정 유저 조회 (ID로 검색)
    * 인증된 사용자만 호출 가능
    """
    # 보안 강화: 만약 '내 정보'만 보게 하려면 아래 주석을 해제하세요.
    # if current_user.id != user_id:
    #     raise HTTPException(status_code=403, detail="권한이 없습니다.")

    # .eq("컬럼명", 값) -> WHERE user_id = 값
    response = supabase.table("users").select("*").eq("user_id", user_id).execute()

    # 데이터가 비어있으면(유저가 없으면) 404 에러 발생
    if not response.data:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    # Supabase는 리스트 형태([])로 반환하므로 첫 번째 요소([0])를 리턴
    return response.data[0]