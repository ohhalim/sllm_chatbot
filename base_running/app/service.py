from typing import List, Optional
from . import repository, schemas

class ItemService:
    """
    비즈니스 로직 계층(Business Logic Layer)입니다.
    Repository를 통해 받은 데이터를 가공하거나, 비즈니스 규칙을 적용합니다.
    """
    def __init__(self, repo: repository.ItemRepository):
        self.repo = repo

    def get_all_items(self) -> List[schemas.Item]:
        """모든 아이템을 조회하는 비즈니스 로직을 처리합니다."""
        items_data = self.repo.get_all()
        # Pydantic v2부터는 .from_orm() 대신 .model_validate() 사용이 권장됩니다.
        return [schemas.Item.model_validate(item) for item in items_data]

    def get_item_by_id(self, item_id: int) -> Optional[schemas.Item]:
        """ID로 특정 아이템을 조회하는 비즈니스 로직을 처리합니다."""
        item_data = self.repo.get_by_id(item_id)
        if item_data:
            return schemas.Item.model_validate(item_data)
        return None

    def create_item(self, item_create: schemas.ItemCreate) -> schemas.Item:
        """
        새로운 아이템을 생성하는 비즈니스 로직을 처리합니다.
        (예: 아이템 이름이 중복되는지 확인하는 로직을 여기에 추가할 수 있습니다.)
        """
        new_item_data = self.repo.create(item_create)
        return schemas.Item.model_validate(new_item_data)

    def update_item(self, item_id: int, item_update: schemas.ItemCreate) -> Optional[schemas.Item]:
        """아이템을 수정하는 비즈니스 로직을 처리합니다."""
        updated_item_data = self.repo.update(item_id, item_update)
        if updated_item_data:
            return schemas.Item.model_validate(updated_item_data)
        return None

    def delete_item(self, item_id: int) -> bool:
        """아이템을 삭제하는 비즈니스 로직을 처리합니다."""
        return self.repo.delete(item_id)

# Repository 인스턴스를 주입하여 Service 인스턴스를 생성합니다.
item_service = ItemService(repo=repository.item_repo)
