import sqlite3


class SQLite:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def create_Nicknames_table(self):
        self.cur.execute("Create Table if not exists Nicknames("
                         "id integer PRIMARY KEY AUTOINCREMENT NOT NULL,"
                         "nickname varchar(32),"
                         "chat_id int"
                         ")")

    def insert_nickname(self, nickname, chat_id):
        self.cur.execute("Insert into Nicknames(nickname, chat_id) values(?,?);",
                         (nickname, chat_id))
        self.conn.commit()

    def select_all_nickname(self):
        self.cur.execute("Select DISTINCT nickname from Nicknames")
        return self.cur.fetchall()

    def is_empty(self):
        self.cur.execute("Select count(*) from Nicknames")
        return self.cur.fetchone()[0] == 0

    def get_chat_id_list_by_nickname(self, nickname):
        self.cur.execute(f"Select chat_id from Nicknames where nickname='{nickname}'")
        return self.cur.fetchall()

    def get_nickname_list_for_chat_id(self, chat_id):
        self.cur.execute(f"Select nickname from Nicknames where chat_id='{chat_id}'")
        return self.cur.fetchall()

    def exists_nickname_for_chat(self, nickname, chat_id):
        self.cur.execute(f"Select count(*) from Nicknames where nickname='{nickname}'and chat_id='{chat_id}'")
        return self.cur.fetchone()[0] > 0

    def delete_nickname(self, nickname, chat_id):
        self.cur.execute(f"Delete from Nicknames where nickname='{nickname}' and chat_id='{chat_id}'")
        self.conn.commit()
