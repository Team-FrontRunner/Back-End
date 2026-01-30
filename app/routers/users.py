## 사용자 회원가입, 개인 정보 등을 다루는 모듈입니다.

from fastapi import APIRouter, HTTPException
from app.db.session import supabase
from app.schemas.user_dto import KakaoLoginRequest, UserResponse
import uuid

# prefix="/users" -> 이 파일의 모든 API 주소 앞에 /users가 자동으로 붙음
# tags=["users"] -> Swagger UI에서 'users' 그룹으로 묶임
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    """모든 유저 조회"""
    response = supabase.table("users").select("*").execute()
    return response.data

@router.post("/login/kakao", response_model=UserResponse)
async def login_with_kakao_mock(request: KakaoLoginRequest):
    """
    [해커톤 데모용] 카카오 로그인 흉내내기 (Mock API)
    어떤 토큰을 보내든 '김할머니'로 로그인 성공 처리합니다.
    """

    # 1. [Mocking] 카카오 서버 통신 대신, 가짜 유저 데이터 생성
    # 해커톤 시연을 위해 항상 같은 유저 정보를 사용하거나,
    # 토큰 값에 따라 다른 유저인 척 할 수도 있습니다.

    fake_user_profile = {
        "email": "demo_grandma@halmaepedia.com",  # 고정된 테스트 계정
        "name": "김순자 할머니",
        "profile_image": "https://placehold.co/200x200/png", # 임시 이미지
        "region": "세종특별자치시",
        "current_point": 3500  # 시연용 초기 포인트
    }

    try:
        # 2. Supabase SDK를 사용해 DB에 'Upsert' (없으면 생성, 있으면 업데이트)
        # email을 기준(Unique Key)으로 유저를 찾습니다.

        # 먼저 이메일로 유저가 있는지 확인
        existing_user = supabase.table("users").select("*").eq("email", fake_user_profile["email"]).execute()

        if existing_user.data:
            # [이미 가입된 경우] -> 정보 업데이트 (로그인)
            user_id = existing_user.data[0]['user_id']

            # 포인트는 덮어쓰지 않고 유지하고 싶다면 update 데이터에서 제외
            update_data = {
                "name": fake_user_profile["name"],
                "profile_image": fake_user_profile["profile_image"],
                "region": fake_user_profile["region"]
            }

            data = supabase.table("users").update(update_data).eq("user_id", user_id).select().execute()
            result_user = data.data[0]

        else:
            # [신규 가입인 경우] -> 데이터 생성
            # user_id는 DB가 자동생성(UUID)하도록 맡깁니다.
            data = supabase.table("users").insert(fake_user_profile).select().execute()
            result_user = data.data[0]

        # 3. 결과 반환
        return result_user

    except Exception as e:
        print(f"Mock Login Error: {str(e)}")
        # 해커톤 때는 에러 내용을 상세히 보여주는 게 디버깅에 좋습니다.
        raise HTTPException(status_code=500, detail=f"로그인 처리 실패: {str(e)}")