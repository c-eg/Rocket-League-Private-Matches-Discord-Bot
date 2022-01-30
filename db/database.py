# -*- coding: utf-8 -*-

from os.path import isfile
from sqlite3 import connect

from apscheduler.triggers.cron import CronTrigger

DB_PATH = "./db/database.db"
DDL_PATH = "./db/DDL.sql"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()


def with_commit(func):
    """
    Commits to the database, usage: @with_commit
    """

    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()

    return inner


@with_commit
def build():
    """
    Creates all necessary tables in sqlite3 database
    :return: void
    """
    if isfile(DDL_PATH):
        scriptexec(DDL_PATH)


def commit():
    """
    Commits to the database
    :return: void
    """
    cxn.commit()


def auto_save(scheduler):
    """
    Commits data to the database
    :param scheduler: scheduler
    :return: void
    """
    scheduler.add_job(commit, CronTrigger(second=0))


def close():
    """
    Closes the connection to the database
    :return: void
    """
    cxn.close()


def field(command, *values):
    """
    Gets the first field from a row
    :param command: SQL to run
    :param values: args
    :return: first field in first row
    """
    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]
    return None


def record(command, *values):
    """
    Gets a single record from the database
    :param command: SQL to run
    :param values: args
    :return: row from database
    """
    cur.execute(command, tuple(values))

    return cur.fetchone()


def records(command, *values):
    """
    Gets multiple records from the database
    :param command: SQL to run
    :param values: args
    :return: rows from database
    """
    cur.execute(command, tuple(values))

    return cur.fetchall()


def column(command, *values):
    """
    Gets the first column from all rows matching the SQL query
    :param command: SQL to run
    :param values: args
    :return: first column of all rows
    """
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]


def execute(command, *values):
    """
    Runs an SQL command
    :param command: SQL to run
    :param values: args
    :return: void
    """
    cur.execute(command, tuple(values))


def multiexec(command, valueset):
    """
    Executes the same command many times
    :param command: command to execute
    :param valueset: sequence of parameters
    :return:
    """
    cur.executemany(command, valueset)


def scriptexec(path):
    """
    Executes multiple SQL statements at once
    :param path: path to SQL statements
    :return: void
    """
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())
