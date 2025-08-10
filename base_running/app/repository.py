from typing import List, Dict, Any, Optional
from . import schemas

# --- In-Memory Database ---
# 간단한 예제를 위해 데이터를 파이썬 리스트에 저장합니다.
# 실제 애플리케이션에서는 이 부분이 데이터베이스(e.g., PostgreSQL, MySQL)와 상호작용하는 코드로 대체됩니다.
_db: List[Dict[str, Any]] = [
    {"id": 1, "name": "MacBook Pro", "description": "A powerful laptop for developers."},
    {"id": 2, "name": "Ergonomic Keyboard", "description": "A comfortable mechanical keyboard."},
]
_next_id = 3


class ItemRepository:
    """
    데이터 영속성 계층(Data Persistence Layer)입니다.
    데이터베이스에 직접 접근하여 CRUD를 수행합니다.
    """
    def get_all(self) -> List[Dict[str, Any]]:
        """모든 아이템을 데이터베이스에서 조회합니다."""
        return _db

    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """ID로 특정 아이템을 데이터베이스에서 조회합니다."""
        return next((item for item in _db if item["id"] == item_id), None)

    def create(self, item_create: schemas.ItemCreate) -> Dict[str, Any]:
        """새로운 아이템을 데이터베이스에 생성합니다."""
        global _next_id
        new_item_data = item_create.dict()
        new_item_data["id"] = _next_id
        _db.append(new_item_data)
        _next_id += 1
        return new_item_data

    def update(self, item_id: int, item_update: schemas.ItemCreate) -> Optional[Dict[str, Any]]:
        """ID로 특정 아이템을 데이터베이스에서 수정합니다."""
        for i, item in enumerate(_db):
            if item["id"] == item_id:
                updated_data = item_update.dict()
                updated_data["id"] = item_id
                _db[i] = updated_data
                return updated_data
        return None

    def delete(self, item_id: int) -> bool:
        """ID로 특정 아이템을 데이터베이스에서 삭제합니다."""
        item_index = next((index for index, item in enumerate(_db) if item["id"] == item_id), None)
        if item_index is not None:
            _db.pop(item_index)
            return True
        return False

# 애플리케이션 전체에서 단일 인스턴스를 사용하도록 생성 (싱글톤 패턴)
item_repo = ItemRepository()
