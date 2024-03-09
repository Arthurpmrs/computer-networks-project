import sqlite3
import logging
import traceback
from pathlib import Path
from .config import CONFIG_FOLDER, SERVER_PORT
Connection = sqlite3.Connection


class DatabaseConnector:
    DB_PATH: Path = CONFIG_FOLDER / "nfs.db"

    def __init__(self):
        self.con = sqlite3.connect(self.DB_PATH)
        self.con.row_factory = sqlite3.Row
        DatabaseConnector.create_tables(self.con)

    def __enter__(self):
        return self.con

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        self.con.close()

    @staticmethod
    def create_tables(con) -> None:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS SavedHosts (
                host_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                ip TEXT NOT NULL UNIQUE,
                port INTEGER NOT NULL,
                added_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                modified_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_connected BOOLEAN
                )""")
        
class DBhandler:
    def __init__(self, con: Connection) -> None:
        self.con = con
        self.logger = logging.getLogger(__name__)

    def add_host(self, name: str, ip: str, port: int = SERVER_PORT) -> None:
        cur = self.con.cursor()
        try:
            cur.execute("""INSERT INTO SavedHosts 
                        (name, ip, port, added_date, modified_date, is_connected) 
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)""", (name, ip, port))
            self.con.commit()
        except sqlite3.IntegrityError:
            self.logger.error("Host already exists.")
            self.con.rollback()
        except Exception:
            self.logger.error("Error adding host.")
            self.logger.error(traceback.format_exc())
            self.con.rollback()

    def get_hosts(self) -> list[dict]:
        cur = self.con.cursor()
        cur.execute("SELECT * FROM SavedHosts")
        hosts: list[dict] = []
        
        for host in cur.fetchall():
            hosts.append(dict(host))
        
        return hosts
    
    def get_host_by_id(self, host_id: int) -> dict:
        cur = self.con.cursor()
        cur.execute("SELECT * FROM SavedHosts WHERE host_id=?", (host_id,))
        row = cur.fetchone()
        
        if row is None:
            raise ValueError("Host ID does not exist!")
        
        return dict(row)