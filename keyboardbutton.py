"""
buttons reply
"""
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def create_subscription_buttons(channels):
    """
    :param channels:
    :return:
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    for channel_name, url, channel_id in channels:
        button_text = f"Azo bo'lish: {channel_name}"
        keyboard.add(InlineKeyboardButton(button_text, url=url))
    keyboard.add(InlineKeyboardButton("Tekshirish", callback_data="tekshirish"))
    return keyboard


def keyboardbutton(btns, resize_keyboard=True, row=1):
    """
    :param btns:
    :param resize_keyboard:
    :param row:
    :return:
    """
    btns = [btns[i:i + row] for i in range(0, len(btns), row)]
    btns = ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=resize_keyboard, row_width=row)
    return btns
