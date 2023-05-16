"""
states
"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class Admin_state(StatesGroup):
    """
    admin all states
    """
    main_menu = State()
    second_menu = State()
    third_menu = State()
    fourth_menu = State()

    add_new_day = State()
    add_new_media_type = State()
    add_new_media = State()


class User_state(StatesGroup):
    """
    user all states
    """
    main_menu = State()
    join_team = State()
    create_team = State()
    creator_pubg_id = State()
    team_settings = State()
    delete_team = State()
    team_pubgers = State()
    pubger = State()
    join_team_pubg_id = State()
    join_team_pubger_name = State()
    pubger_menu = State()
