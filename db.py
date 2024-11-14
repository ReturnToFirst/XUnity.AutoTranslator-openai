import sqlite3
from dataclasses import dataclass

@dataclass
class DB:
    connector: sqlite3.Connection
    cursor: sqlite3.Cursor

    @classmethod
    def from_file(cls, db_file: str):
        connector = sqlite3.connect(db_file)
        cursor = connector.cursor()

        if "translations" not in cls.get_table_list(cursor):
            cls.init_table(cursor)

        return cls(connector, cursor)
        
    @classmethod
    def get_table_list(cls, cursor: sqlite3.Cursor) -> list:
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")
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

    def get_latest_translation(self, index: int):
        self.cursor.execute(f"SELECT * FROM translations ORDER BY rowid desc LIMIT {index}")
        result = self.cursor.fetchall()
        return [TranslationRecord(single_result[0], single_result[1], single_result[2], single_result[3]) for single_result in result]
@dataclass
class TranslationRecord:
    src_lang: str
    tgt_lang: str
    src_text: str
    tgt_text: str