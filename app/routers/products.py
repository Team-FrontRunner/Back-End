from fastapi import APIRouter, HTTPException
from typing import List
from app.db.session import supabase
# 파일명이 product_dto.py라면 아래와 같이 수정, products_dto.py라면 그대로 두세요.
from app.schemas.products_dto import ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("/", response_model=List[ProductResponse], summary="쇼핑몰 데이터 가져오기")
def get_products():
    """
    Supabase 상의 products 테이블의 값을 불러와 프론트엔드에 전송합니다.
    """
    try:
        response = supabase.table("products").select("*").execute()

        # 디버깅을 위해 콘솔에 출력해 봅니다 (개발 중에만 사용)
        print(f"Fetched Data: {response.data}")

        return response.data
    except Exception as e:
        # 에러 내용을 더 자세히 봅니다.
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))