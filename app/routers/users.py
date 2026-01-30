## 사용자 회원가입, 개인 정보 등을 다루는 모듈입니다.

from fastapi import APIRouter, HTTPException, Depends
from app.db.session import supabase
from app.schemas.users_dto import UserResponse, LoginRequest, TokenResponse
from app.core.deps import get_current_user
from app.core.security import create_access_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/login", response_model=TokenResponse)
def login_with_id(request: LoginRequest):
    """
    [개발용] User ID로 로그인하여 토큰 발급
    * Supabase Auth가 아닌, 백엔드 자체 JWT 토큰을 발급합니다.
    """
    # 1. DB에 해당 user_id가 존재하는지 확인
    response = supabase.table("users").select("*").eq("user_id", request.user_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="존재하지 않는 User ID입니다.")
    
    user = response.data[0]
    
    # 2. 토큰 생성 (sub에 user_id 저장)
    access_token = create_access_token(data={"sub": user["user_id"]})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_my_info(current_user: dict = Depends(get_current_user)):
    """
    내 정보 조회
    * 로그인한 사용자의 상세 정보를 반환합니다.
    """
    # get_current_user가 이미 DB에서 유저 정보를 가져와서 반환하므로 그대로 리턴
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, current_user = Depends(get_current_user)): 
    """
    특정 유저 조회 (ID로 검색)
    * 인증된 사용자만 호출 가능
    """
    response = supabase.table("users").select("*").eq("user_id", user_id).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    return response.data[0]

@router.get("/")
def get_users(current_user = Depends(get_current_user)):
    """
    모든 유저 조회
    * 인증된(로그인한) 사용자만 호출 가능합니다.
    """
    response = supabase.table("users").select("*").execute()
    return response.data