import sys
import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client, Client

# 환경 변수 로드
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: .env 파일이 없거나 SUPABASE_URL/KEY가 설정되지 않았습니다.")
    sys.exit(1)

# Supabase 클라이언트 생성
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_test_token():
    email = "testuser@example.com"
    password = "testpassword123!"

    print(f"Attempting to sign in with {email}...")

    try:
        # 1. 로그인 시도
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        print("\nLogin Successful!")
        print("-" * 50)
        print(f"Access Token:\n{res.session.access_token}")
        print("-" * 50)
        print("위 토큰을 복사해서 Authorization 헤더에 사용하세요.")
        print("Format: 'Bearer <Access Token>'")

    except Exception as e:
        # 로그인 실패 시 회원가입 시도
        print(f"\nLogin failed ({str(e)}). Attempting to sign up...")
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            if res.user:
                print("\nSign up successful! Please check your email/console if email confirmation is enabled.")
                # 자동 로그인이 되는 경우도 있지만, 이메일 확인이 필요한 경우 토큰이 없을 수 있음
                if res.session:
                    print("-" * 50)
                    print(f"Access Token:\n{res.session.access_token}")
                    print("-" * 50)
                else:
                    print("회원가입은 되었으나 세션이 없습니다. 이메일 인증 설정을 확인하거나 인증 끄기(Auto Confirm)를 해주세요.")
            else:
                print("Sign up returned no user.")
        except Exception as signup_error:
            print(f"Sign up also failed: {str(signup_error)}")

if __name__ == "__main__":
    asyncio.run(get_test_token())
