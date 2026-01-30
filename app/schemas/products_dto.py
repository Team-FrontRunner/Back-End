## 상품 관련 입출력 모듈입니다.

from pydantic import BaseModel
from typing import Optional

class ProductResponse(BaseModel):
    item_id: int
    name: str
    price: int
    image_url: Optional[str] = None
    category: str
    quantity: int

    class Config:
        from_attributes = True
