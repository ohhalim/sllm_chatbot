from pydantic import BaseModel
from typing import Optional

# --- Base Schemas ---
# 다른 스키마들이 상속받을 기본 모델입니다.
# 공통 필드를 여기에 정의합니다.
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None


# --- Create Schema ---
# 아이템을 '생성'할 때 요청(request) 본문에서 사용할 모델입니다.
# id는 서버에서 자동 생성하므로 여기에는 포함되지 않습니다.
class ItemCreate(ItemBase):
    pass


# --- Read/Response Schema ---
# 클라이언트에게 '응답(response)'할 때 사용할 모델입니다.
# 데이터베이스에 저장된 완전한 아이템 정보를 나타냅니다. (id 포함)
class Item(ItemBase):
    id: int

    # Pydantic V2+ 에서는 from_attributes=True 를 사용합니다.
    # 이는 SQLAlchemy 같은 ORM 모델 객체를 Pydantic 모델로 변환할 수 있게 해줍니다.
    # 예: db_item 객체를 Item(**db_item.__dict__) 대신 Item.from_orm(db_item) 으로 변환 가능
    class Config:
        from_attributes = True
