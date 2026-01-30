## 주문 관련 데이터 모델입니다.

from pydantic import BaseModel

# [요청] 상품 주문 시 받는 데이터
class OrderRequest(BaseModel):
    # user_id는 URL 경로에서 받으므로 body에서는 제외될 수도 있지만,
    # 명세서(image_66107b)에 포함되어 있다면 넣습니다. (보통은 URL param을 우선합니다)
    # 여기서는 스키마 매칭을 위해 포함하되, 실제 로직에선 URL의 user_id를 사용하겠습니다.
    user_id: str
    item_id: int
    used_point: int

# [응답] 주문 완료 후 보낼 데이터
class OrderResponse(BaseModel):
    order_id: int
    remaining_point: int
    status: str