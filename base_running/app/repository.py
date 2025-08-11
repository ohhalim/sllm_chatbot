import os
from typing import List, Dict, Any, Optional

import psycopg
from psycopg.rows import dict_row

from . import schemas


# --- PostgreSQL Connection ---
# DATABASE_URL 예: postgres://user:password@localhost:5432/mydb
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # 개발 편의를 위해 기본값을 허용할 수도 있으나, 안전을 위해 명시적으로 요구합니다.
    # 필요 시 아래 주석을 해제하고 기본값을 사용하세요.
    # DATABASE_URL = "postgres://postgres:postgres@localhost:5432/postgres"
    raise RuntimeError("환경변수 DATABASE_URL 이(가) 설정되어 있지 않습니다.")


def _ensure_table_exists() -> None:
    """필요 시 items 테이블을 생성합니다."""
    create_sql = """
    CREATE TABLE IF NOT EXISTS items (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    );
    """
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(create_sql)
        conn.commit()


class ItemRepository:
    """
    데이터 영속성 계층(Data Persistence Layer)입니다.
    PostgreSQL을 사용하여 CRUD를 수행합니다.
    """

    def __init__(self) -> None:
        _ensure_table_exists()

    def get_all(self) -> List[Dict[str, Any]]:
        """모든 아이템을 데이터베이스에서 조회합니다."""
        sql = "SELECT id, name, description FROM items ORDER BY id;"
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                return list(rows)

    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """ID로 특정 아이템을 데이터베이스에서 조회합니다."""
        sql = "SELECT id, name, description FROM items WHERE id = %s;"
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (item_id,))
                row = cur.fetchone()
                return dict(row) if row else None

    def create(self, item_create: schemas.ItemCreate) -> Dict[str, Any]:
        """새로운 아이템을 데이터베이스에 생성합니다."""
        data = item_create.dict()
        sql = """
            INSERT INTO items (name, description)
            VALUES (%s, %s)
            RETURNING id, name, description;
        """
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data.get("name"), data.get("description")))
                row = cur.fetchone()
            conn.commit()
        return dict(row)

    def update(self, item_id: int, item_update: schemas.ItemCreate) -> Optional[Dict[str, Any]]:
        """ID로 특정 아이템을 데이터베이스에서 수정합니다."""
        data = item_update.dict()
        sql = """
            UPDATE items
            SET name = %s,
                description = %s
            WHERE id = %s
            RETURNING id, name, description;
        """
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data.get("name"), data.get("description"), item_id))
                row = cur.fetchone()
            conn.commit()
        return dict(row) if row else None

    def delete(self, item_id: int) -> bool:
        """ID로 특정 아이템을 데이터베이스에서 삭제합니다."""
        sql = "DELETE FROM items WHERE id = %s RETURNING id;"
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (item_id,))
                row = cur.fetchone()
            conn.commit()
            return row is not None

# 애플리케이션 전체에서 단일 인스턴스를 사용하도록 생성 (싱글톤 패턴)
item_repo = ItemRepository()