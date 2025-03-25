import sqlite3
import psycopg
from dataclasses import dataclass, field
from typing import Union
from config import DatabaseConfig

@dataclass
class DB:
    connector: Union[sqlite3.Connection, psycopg.Connection]
    cursor: Union[sqlite3.Cursor, psycopg.Cursor]
    db_config: DatabaseConfig

    @classmethod
    def from_config(cls, db_config: DatabaseConfig):
        match db_config.db_type:
            case "sqlite":
                connector = sqlite3.connect(db_config.sqlite_config.db_path)
            case "postgres":
                connector = psycopg.connect("""host={}
                                            port={}
                                            dbname={}
                                            user={}
                                            password={}
                                             """.format(db_config.postgres_config.host,
                                                        db_config.postgres_config.port,
                                                        db_config.postgres_config.db,
                                                        db_config.postgres_config.user,
                                                        db_config.postgres_config.password)
                                            )
        cls.db_config = db_config
        cls.connector = connector
        cls.cursor = connector.cursor()
        if "translations" not in cls.get_table_list():
            cls.init_table()

        return cls(cls.connector, cls.cursor, cls.db_config)
        
    @classmethod
    def get_table_list(cls) -> list:
        match cls.db_config.db_type:
            case "sqlite":
                query = """SELECT name FROM sqlite_master
                        WHERE type = 'table'
                        AND name NOT LIKE 'sqlite_%'
                        """
            case "postgres":
                query = """SELECT tablename FROM pg_catalog.pg_tables
                        WHERE schemaname
                        NOT IN ('pg_catalog', 'information_schema')
                        """

        cls.cursor.execute(query)
        return [t[0] for t in cls.cursor.fetchall()]

    @classmethod
    def init_table(cls) -> None:
        cls.cursor.execute("""CREATE TABLE translations (
                            src_lang TEXT,
                            tgt_lang TEXT,
                            src_text TEXT,
                            tgt_text TEXT)
                           """)
        cls.cursor.connection.commit()
        
    def save_translation(cls, src_lang:str, tgt_lang:str, src_text:str, tgt_text:str) -> None:
        query = """
                INSERT INTO translations
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})
                """
        cls.cursor.execute(cls._fill_placeholder(query), (src_lang, tgt_lang, src_text, tgt_text))
        cls.connector.commit()

    def fetch_translation(cls, src_lang:str, tgt_lang:str, src_text:str) -> str:
        query = """
            SELECT tgt_text FROM translations 
            WHERE src_lang = {placeholder}
            AND tgt_lang = {placeholder} 
            AND src_text = {placeholder}
        """

        cls.cursor.execute(cls._fill_placeholder(query), (src_lang, tgt_lang, src_text))
        result = cls.cursor.fetchone()
        return result[0] if result else None

    def delete_translation(cls, src_lang:str , tgt_lang:str, src_text:str) -> None:
        query = """
                DELETE FROM translations
                WHERE src_lang={placeholder}
                AND tgt_lang={placeholder}
                AND src_text={placeholder}
                """

        cls.cursor.execute(cls._fill_placeholder(query), (src_lang, tgt_lang, src_text))
        cls.connector.commit()

    def get_latest_translations(cls, src_lang: str, tgt_lang: str, index: int):
        query = """
                SELECT * FROM translations 
                WHERE src_lang = {placeholder} AND tgt_lang = {placeholder} 
                ORDER BY {order_by} DESC 
                LIMIT {placeholder}
                """
                
        cls.cursor.execute(cls._fill_placeholder(query), (src_lang, tgt_lang, index))
        records = cls.cursor.fetchall()

        return [TranslationRecord(record[0], record[1], record[2], record[3]) for record in records]
    
    @classmethod
    def _fill_placeholder(cls, target_str: str):
        match cls.db_config.db_type:
            case "sqlite":
                placeholder = "?"
                order_by = "rowid"
            case "postgres":
                placeholder = "%s"
                order_by = "ctid"

        return target_str.format(placeholder=placeholder, order_by=order_by)

@dataclass
class TranslationRecord:
    src_lang: str
    tgt_lang: str
    src_text: str
    tgt_text: str