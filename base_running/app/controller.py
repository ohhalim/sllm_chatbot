from fastapi import APIRouter, HTTPException, Depends
from typing import List
from . import service, schemas

# --- Dependency Injection ---
# FastAPI의 Depends를 사용하여 Service 계층의 의존성을 주입합니다.
# 이렇게 하면 컨트롤러가 특정 서비스 인스턴스에 직접 의존하지 않게 되어
# 코드의 재사용성과 테스트 용이성이 높아집니다.
def get_item_service() -> service.ItemService:
    return service.item_service

# --- API Router ---
# API 엔드포인트를 정의하는 라우터입니다.
router = APIRouter(
    prefix="/items",  # 이 라우터의 모든 경로는 "/items"로 시작합니다.
    tags=["Items"],   # API 문서에서 "Items" 태그로 그룹화됩니다.
)

@router.post("/", response_model=schemas.Item, status_code=201)
def create_item_endpoint(
    item: schemas.ItemCreate,
    svc: service.ItemService = Depends(get_item_service)
):
    """새로운 아이템을 생성합니다."""
    return svc.create_item(item_create=item)

@router.get("/", response_model=List[schemas.Item])
def read_items_endpoint(svc: service.ItemService = Depends(get_item_service)):
    """모든 아이템 목록을 조회합니다."""
    return svc.get_all_items()

@router.get("/{item_id}", response_model=schemas.Item)
def read_item_endpoint(
    item_id: int,
    svc: service.ItemService = Depends(get_item_service)
):
    """특정 ID의 아이템을 조회합니다."""
    db_item = svc.get_item_by_id(item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.Item)
def update_item_endpoint(
    item_id: int,
    item: schemas.ItemCreate,
    svc: service.ItemService = Depends(get_item_service)
):
    """특정 ID의 아이템을 수정합니다."""
    updated_item = svc.update_item(item_id=item_id, item_update=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{item_id}", response_model=dict)
def delete_item_endpoint(
    item_id: int,
    svc: service.ItemService = Depends(get_item_service)
):
    """특정 ID의 아이템을 삭제합니다."""
    if not svc.delete_item(item_id=item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
