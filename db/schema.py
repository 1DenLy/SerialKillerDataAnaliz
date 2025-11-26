import sqlite3
import logging

logger = logging.getLogger(__name__)

# Читаемый SQL без лишних символов
INIT_SCRIPT = """
CREATE TABLE IF NOT EXISTS agencies (
    ori TEXT PRIMARY KEY,
    state TEXT,
    agency_name TEXT,
    agency_type TEXT,
    source TEXT,
    cnty_fips TEXT,
    msa TEXT
);

CREATE TABLE IF NOT EXISTS weapons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS homicides (
    id TEXT PRIMARY KEY,
    ori TEXT,
    year INTEGER,
    month TEXT,
    weapon_id INTEGER,
    relationship_id INTEGER,
    vic_age INTEGER,
    vic_sex TEXT,
    vic_race TEXT,
    off_age INTEGER,
    off_sex TEXT,
    solved TEXT,
    FOREIGN KEY (ori) REFERENCES agencies (ori),
    FOREIGN KEY (weapon_id) REFERENCES weapons (id),
    FOREIGN KEY (relationship_id) REFERENCES relationships (id)
);
"""

def init_db_schema(conn: sqlite3.Connection) -> None:
    """Применяет схему базы данных."""
    try:
        conn.executescript(INIT_SCRIPT)
        logger.info("Схема базы данных успешно обновлена/проверена.")
    except sqlite3.Error as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
        raise