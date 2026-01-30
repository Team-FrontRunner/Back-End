## 사용자 회원가입, 개인 정보 등을 다루는 모듈입니다.

from fastapi import APIRouter, HTTPException
from app.db.session import supabase
from app.schemas.users_dto import KakaoLoginRequest, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/login/kakao", response_model=UserResponse)
async def login_with_kakao_mock(request: KakaoLoginRequest):
    """
    [해커톤 데모용] Mock Login
    user 테이블에 email 컬럼이 없으므로, 토큰별로 고정된 UUID를 사용하여 로그인 처리합니다.
    """
    if request.access_token == "user1":
        # 박춘자 할머니 (메인 데모용)
        mock_user = {
            "user_id": "00000000-0000-0000-0000-000000000001",  # 고정 UUID
            "name": "박춘자",
            "profile_image": "https://placehold.co/200x200/png?text=Grandma",
            "region": "세종특별자치시",
            "current_point": 3500
        }
    elif request.access_token == "user2":
        # 정광팔 할아버지
        mock_user = {
            "user_id": "00000000-0000-0000-0000-000000000002",
            "name": "정광팔",
            "profile_image": "https://placehold.co/200x200/png?text=Grandpa",
            "region": "대전광역시",
            "current_point": 1200
        }
    else:
        # 그 외 토큰 (체험용) -> 랜덤 UUID를 쓰면 계속 새 유저가 생기므로 주의
        mock_user = {
            "user_id": "00000000-0000-0000-0000-000000000099",
            "name": "tester",
            "profile_image": None,
            "region": "서울특별시 강남구",
            "current_point": 100000000
        }

    try:
        # 2. Supabase DB에 Upsert 실행
        # 로직: user_id가 PK이므로, 이 ID를 가진 데이터가 있으면 Update, 없으면 Insert 합니다.

        response = supabase.table("users").upsert(mock_user).select().execute()

        # 3. 결과 반환
        if response.data:
            return response.data[0]
        else:
            raise HTTPException(status_code=500, detail="데이터 저장 후 반환된 값이 없습니다.")

    except Exception as e:
        print(f"Login Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"로그인 실패: {str(e)}")
@router.get("/")
def get_users():
    """모든 유저 조회"""
    response = supabase.table("users").select("*").execute()
    return response.data