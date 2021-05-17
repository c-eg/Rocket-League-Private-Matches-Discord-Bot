# -*- coding: utf-8 -*-
from bot.db.database import Database


def main():
    db = Database('bot/db/database.db')

    sql = """CREATE TABLE IF NOT EXISTS player (
    discord_id INTEGER PRIMARY KEY,
    mmr INTEGER NOT NULL
    )"""

    db.cursor.execute(sql)

    # db.create_tables('bot/db/DDL.sql')


if __name__ == '__main__':
    main()
