# 가장 먼저 스키마 로 데이터의 형태를 정의 
# 데이터의 구조를 먼저 정의하면 이후 계층들이 어떤 데이터를 다룰지 명확해짐
from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass 

class Item(ItemBase):
 id: int

class Config:
    from_attributes =True
