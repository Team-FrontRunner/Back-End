from fastapi import APIRouter, HTTPException
from typing import List
from app.db.session import supabase
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
        return response.data
    except Exception as e:
        # 실제 운영 환경에서는 로깅을 추가하는 것이 좋습니다.
        raise HTTPException(status_code=500, detail=str(e))
