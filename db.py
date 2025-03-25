import sqlite3
import psycopg
from dataclasses import dataclass, field
from typing import Union
from config import DatabaseConfig

@dataclass
class DB:
    connector: Union[sqlite3.Connection]
    cursor: Union[sqlite3.Cursor, psycopg.Cursor]
    db_config: DatabaseConfig = field(init=False)

    @classmethod
    def from_config(cls, db_config: DatabaseConfig):
        cls.db_config = db_config
        match cls.db_config.db_type:
            case "sqlite":
                connector = sqlite3.connect(db_config.sqlite_config.db_path)
            case "postgres":
                connector = psycopg.connect("host=%s port=%d dbname=%s user=%s password=%s".format(cls.db_config.postgres_config.host,
                                                                                    cls.db_config.postgres_config.port,
                                                                                    cls.db_config.postgres_config.db,
                                                                                    cls.db_config.postgres_config.user,
                                                                                    cls.db_config.postgres_config.password))
        cursor = connector.cursor()

        if "translations" not in cls.get_table_list(cursor):
            cls.init_table(cursor)

        return cls(connector, cursor)
        
    @classmethod
    def get_table_list(cls, cursor: Union[sqlite3.Cursor, psycopg.Cursor]) -> list:
        match cls.db_config.db_type:
            case "sqlite":
                query = "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            case "postgres":
                query = "SELECT * FROM information_schema.tables"

        cursor.execute(query)
        return [t[0] for t in cursor.fetchall()]

    @classmethod
    def init_table(cls, cursor: sqlite3.Cursor):
        cursor.execute("""CREATE TABLE translations (
                        src_lang TEXT,
                        tgt_lang TEXT,
                        src_text TEXT,
                        tgt_text TEXT)""")
        cursor.connection.commit()
        
    def save_translation(self, src_lang:str, tgt_lang:str, src_text:str, tgt_text:str):
        self.cursor.execute("INSERT INTO translations VALUES (?,?,?,?)", (src_lang, tgt_lang, src_text, tgt_text))
        self.connector.commit()

    def fetch_translation(self, src_lang:str , tgt_lang:str, src_text:str):
        self.cursor.execute("SELECT tgt_text FROM translations WHERE src_lang=? AND tgt_lang=? AND src_text=?", (src_lang, tgt_lang, src_text))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete_translation(self, src_lang:str , tgt_lang:str, src_text:str):
        self.cursor.execute("DELETE FROM translations WHERE src_lang=? AND tgt_lang=? AND src_text=?", (src_lang, tgt_lang, src_text))
        self.connector.commit()

    def get_latest_translations(self, src_lang: str, tgt_lang: str, index: int):
        self.cursor.execute(f"SELECT * FROM translations WHERE src_lang=? AND tgt_lang=? ORDER BY rowid desc LIMIT {index}", (src_lang, tgt_lang))
        records = self.cursor.fetchall()
        return [TranslationRecord(record[0], record[1], record[2], record[3]) for record in records]

@dataclass
class TranslationRecord:
    src_lang: str
    tgt_lang: str
    src_text: str
    tgt_text: str