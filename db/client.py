import sqlite3
import logging
from pathlib import Path
from typing import Optional, Self

logger = logging.getLogger(__name__)


class SQLiteClient:
    """
    Context Manager для безопасного подключения к SQLite.
    """

    def __init__(self, db_path: Path | str):
        # Приводим путь к Path объекту для надежности
        self.db_path = Path(db_path)
        self.conn: Optional[sqlite3.Connection] = None

    def __enter__(self) -> "SQLiteClient":
        try:
            self.conn = sqlite3.connect(self.db_path)
            # Включаем поддержку внешних ключей (важно для SQLite)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            return self
        except sqlite3.Error as e:
            logger.critical(f"Не удалось подключиться к БД {self.db_path}: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
                logger.error(f"Транзакция откатана (Rollback) из-за ошибки: {exc_type.__name__}")
            else:
                try:
                    self.conn.commit()
                    logger.debug("Транзакция зафиксирована (Commit).")
                except sqlite3.Error as e:
                    logger.error(f"Ошибка при коммите: {e}")
                    self.conn.rollback()

            self.conn.close()
            self.conn = None

    def get_cursor(self) -> sqlite3.Cursor:
        if not self.conn:
            raise ConnectionError("Нет активного подключения к базе данных.")
        return self.conn.cursor()