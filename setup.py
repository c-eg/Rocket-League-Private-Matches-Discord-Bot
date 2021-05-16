# -*- coding: utf-8 -*-
from bot.util.database import Database


def main():
    db = Database('bot/util/database.db')
    db.create_tables('bot/util/DDL.sql')


if __name__ == '__main__':
    main()
