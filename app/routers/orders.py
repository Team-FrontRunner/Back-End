## 상품 주문 및 포인트 결제 로직을 담당하는 모듈입니다.

from fastapi import APIRouter, HTTPException
from app.db.session import supabase
from app.schemas.orders_dto import OrderRequest, OrderResponse

router = APIRouter(
    prefix="/order",
    tags=["order"]
)


@router.post("/{user_id}", response_model=OrderResponse, summary="상품 주문 및 포인트 차감")
def create_order(user_id: str, request: OrderRequest):
    """
    [POST] /api/order/{user_id}
    1. 상품 재고(quantity) 및 가격 확인
    2. 사용자 포인트(current_point) 잔액 확인
    3. 포인트 차감 (users 테이블 update)
    4. 포인트 로그 기록(point_logs) 및 주문 생성(orders)
    """
    try:
        # --- 1단계: 상품 확인 (products 테이블) ---
        # item_id로 상품 조회
        product_res = supabase.table("products").select("*").eq("item_id", request.item_id).execute()

        if not product_res.data:
            raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

        product = product_res.data[0]

        # 가격 검증 (요청된 포인트와 실제 상품 가격이 같은지)
        if product['price'] != request.used_point:
            raise HTTPException(status_code=400, detail="상품 가격과 결제 포인트가 일치하지 않습니다.")

        # 재고 확인 (quantity가 0보다 커야 함)
        if product['quantity'] <= 0:
            raise HTTPException(status_code=400, detail="재고가 부족하여 구매할 수 없습니다.")

        # --- 2단계: 사용자 포인트 확인 (users 테이블) ---
        user_res = supabase.table("users").select("current_point").eq("user_id", user_id).execute()

        if not user_res.data:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        current_user_point = user_res.data[0]['current_point']

        # 잔액 부족 확인
        if current_user_point < request.used_point:
            raise HTTPException(status_code=400, detail="보유 포인트가 부족합니다.")

        # --- 3단계: 포인트 차감 (users 테이블 Update) ---
        remaining_point = current_user_point - request.used_point

        update_user_res = supabase.table("users") \
            .update({"current_point": remaining_point}) \
            .eq("user_id", user_id) \
            .execute()

        if not update_user_res.data:
            raise HTTPException(status_code=500, detail="포인트 차감 중 오류가 발생했습니다.")

        # --- 4단계: 로그 기록 및 주문 생성 ---

        # (4-1) 포인트 로그 기록 (point_logs 테이블)
        # 스키마에 따라 type, amount, description 저장
        log_data = {
            "user_id": user_id,
            "type": "USE",  # 포인트 사용
            "amount": request.used_point,
            "description": f"상품 구매: {product['name']}"
        }
        supabase.table("point_logs").insert(log_data).execute()

        # (4-2) 주문 내역 생성 (orders 테이블)
        # 스키마에 따라 item_id, used_point, status 저장
        order_data = {
            "user_id": user_id,
            "item_id": request.item_id,
            "used_point": request.used_point,  # total_price 대신 스키마의 used_point 사용
            "status": "COMPLETED"
        }

        order_res = supabase.table("orders").insert(order_data).execute()

        if not order_res.data:
            raise HTTPException(status_code=500, detail="주문 생성 실패")

        new_order_id = order_res.data[0]['order_id']

        # (선택 사항) 상품 재고 감소 로직이 필요하다면 여기에 products update 추가 가능

        # --- 최종 응답 반환 ---
        return {
            "order_id": new_order_id,
            "remaining_point": remaining_point,
            "status": "SUCCESS"
        }

    except Exception as e:
        print(f"Order Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))