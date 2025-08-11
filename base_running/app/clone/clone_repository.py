from typing import List, Dict, Any, Optional
from . import schemas 


class ItemRepository:
    def get_all(self) -> List[Dict]

    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]
