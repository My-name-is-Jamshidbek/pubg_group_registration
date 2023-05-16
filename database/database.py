"""
all database functions in here
"""
from config import DATABASE_NAME
import sqlite3


def create_database():
    """
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Guruhlar jadvalini yaratish
    cursor.execute('''CREATE TABLE IF NOT EXISTS guruhlar
                      (_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT,
                       creator_id INTEGER)''')

    # Pubgerlar jadvalini yaratish
    cursor.execute('''CREATE TABLE IF NOT EXISTS pubgerlar
                          (_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           pubg_id INTEGER,
                           name TEXT,
                           guruh_id INTEGER,
                           FOREIGN KEY(guruh_id) REFERENCES guruhlar(_id))''')

    # Userlar jadvalini yaratish
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           tg_id INTEGER,
                           fullname TEXT)'''
                   )
    cursor.execute('''CREATE TABLE IF NOT EXISTS channels
                              (_id INTEGER PRIMARY KEY AUTOINCREMENT,
                               channel_id INTEGER,
                               taklif_havolasi TEXT,
                               name TEXT)'''
                   )
    connection.commit()
    connection.close()


def add_channel(channel_id, name, taklif_havolasi):
    """
    :param channel_id:
    :param name:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM channels WHERE channel_id=?", (channel_id,))
    existing_channel = cursor.fetchone()

    if existing_channel:
        connection.close()
        return False

    cursor.execute("INSERT INTO channels (channel_id, name, taklif_havolasi) VALUES (?, ?, ?)", (channel_id, name,
                                                                                                 taklif_havolasi))
    connection.commit()
    connection.close()
    return True


def get_channels():
    """
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT name, taklif_havolasi, channel_id FROM channels")
    channels = cursor.fetchall()
    connection.close()
    return channels


def team_member_count(team_id):
    """
    :param team_id:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM pubgerlar WHERE guruh_id=?", (team_id,))
    count = cursor.fetchone()[0]
    connection.close()

    return count


def add_user(tg_id, fullname):
    """
    :param tg_id:
    :param fullname:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO users (fullname, tg_id) VALUES (?, ?)", (fullname, tg_id))
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error:
        connection.close()
        return False


def create_team(user_id, name):
    """
    :param user_id:
    :param name:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO guruhlar (name, creator_id) VALUES (?, ?)", (name, user_id))
        team_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return team_id
    except sqlite3.Error:
        connection.close()
        return False


def add_pubger(pubg_id, team_id, name):
    """
    :param pubg_id:
    :param team_id:
    :param name:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO pubgerlar (pubg_id, guruh_id, name) VALUES (?, ?, ?)", (pubg_id, team_id, name))
        connection.commit()
        connection.close()
        return True
    except sqlite3.Error:
        connection.close()
        return False


def del_team(team_id):
    """
    :param team_id:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM guruhlar WHERE _id=?", (team_id,))
    connection.commit()
    connection.close()


def team_pubgers(team_id):
    """
    :param team_id:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM pubgerlar WHERE guruh_id=?", (team_id,))
    pubgers = cursor.fetchall()
    connection.close()

    return [pubger[0] for pubger in pubgers]


def team_pubger(team_id, pubger_id):
    """
    :param team_id:
    :param pubger_id:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM pubgerlar WHERE guruh_id=? AND name=?", (team_id, pubger_id))
    pubger = cursor.fetchone()
    connection.close()

    if pubger:
        pubg_id, _, name, _ = pubger
        return f"Pubger ID: {pubg_id}, Name: {name}"
    else:
        return ""


def del_pubger(team_id, pubger_name):
    """
    :param team_id:
    :param pubger_name:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM pubgerlar WHERE guruh_id=? AND name=?", (team_id, pubger_name))
    connection.commit()
    connection.close()


def search_team(_id):
    """
    :param _id:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM guruhlar WHERE _id=?", (_id,))
    count = cursor.fetchone()[0]
    connection.close()

    return count > 0


def get_team_name(_id):
    """
    :param _id:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM guruhlar WHERE _id=?", (_id,))
    name = cursor.fetchone()[0]
    connection.close()

    return name


def get_team_pubgers(_id):
    """
    :param _id:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT pubg_id, name FROM pubgerlar WHERE guruh_id=?", (_id,))
    pubgers = cursor.fetchall()
    connection.close()

    pubgers_info = "\n".join([f"Pubger ID: {pubg_id}, Name: {name}" for pubg_id, name in pubgers])
    return pubgers_info


def out_team(team_id, pubger_name):
    """
    :param team_id:
    :param pubger_name:
    :return:
    """
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM pubgerlar WHERE guruh_id=? AND name=?", (team_id, pubger_name))
    connection.commit()
    connection.close()
