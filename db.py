import sqlite3
from dataclasses import dataclass

@dataclass
class DB:
    connector: sqlite3.Connection
    cursor: sqlite3.Cursor

    @classmethod
    def from_file(cls,db_file: str):
        return cls(sqlite3.connect(db_file), sqlite3.connect(db_file).cursor())
        

    def get_table_list(self):
        query = self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")
        result = query.fetchone()
        return () if not result else result

    def init_table(self):
        if not "translations" in self.get_table_list():
            self.cursor.execute("""CREATE TABLE translations (
                        src_lang TEXT,
                        tgt_lang TEXT,
                        src_text TEXT,
                        tgt_text TEXT)""")
            self.connector.commit()
        
    def add_translation(self, src_lang:str, tgt_lang:str, src_text:str, tgt_text:str):
        self.cursor.execute("INSERT INTO translations VALUES (?,?,?,?)", (src_lang, tgt_lang, src_text, tgt_text))
        self.connector.commit()

    def fetch_translation(self, src_lang:str , tgt_lang:str, src_text:str):
        self.cursor.execute("SELECT tgt_text FROM translations WHERE src_lang=? AND tgt_lang=? AND src_text=?", (src_lang, tgt_lang, src_text))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete_translation(self, src_lang:str , tgt_lang:str, src_text:str):
        self.cursor.execute("DELETE FROM translations WHERE src_lang=? AND tgt_lang=? AND src_text=?", (src_lang, tgt_lang, src_text))
        self.connector.commit()