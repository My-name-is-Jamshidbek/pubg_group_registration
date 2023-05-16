"""
app file
"""
# imports
from aiogram.types import ContentType as ct

from database import database
from loader import dp, bot
from aiogram.types import Message as m, CallbackQuery as cq, ChatMemberStatus
from keyboardbutton import keyboardbutton, create_subscription_buttons
from states import *
from apps import user
from database.database import add_user


async def check_subscription(user_id, channel_id):
    """
    :param user_id:
    :param channel_id:
    :return:
    """
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status == ChatMemberStatus.MEMBER
    except Exception as e:
        print(f"Xato: {e}")
        return True


# cmd start
async def cmd_start(m: m):
    """
    :param m:
    :return:
    """
    # create_database()
    # if is_admin(_id=m.from_user._id):
    #     await m.answer("Admin botga hush kelibsiz.\nKerakli menyuni tanlashingiz mumkin:",
    #                    reply_markup=keyboardbutton(["Foydalanuvchi oynasi", "Foydalanuvchilar", "Reklamalar"]))
    #     await Admin_state.main_menu.set()
    if False:
        pass
    else:
        # database.create_database()
        # database.add_channel(
        #     channel_id=1697856433,
        #     name="ALISHER PUBGM",
        #     taklif_havolasi="https://t.me/alisherpubg"
        # )
        try:
            username = m.from_user.username
        except Exception as _:
            username = "No username"
        try:
            add_user(tg_id=str(m.from_user.id), fullname=username)
        except Exception as _:
            pass
        await m.answer(f"{m.from_user.full_name} botga hush kelibsiz.\nBot ish faoliyatini davom ettirishi "
                       f"uchun iltimos quyidagi kanallarga obuna bo'ling va tekshirish tugmasini bosing.",
                       reply_markup=create_subscription_buttons(database.get_channels()))


@dp.callback_query_handler(lambda c: c.data == 'tekshirish')
async def process_check_callback(query: cq):
    # Tugma bosilganda ishlayacak logika
    channels_ids = ["@"+i[1].split("/")[-1] for i in database.get_channels()]
    a = True
    for cid in channels_ids:
        if await check_subscription(query.from_user.id, cid):
            a = True
        else:
            a = False
            break
    if a:
        await bot.answer_callback_query(query.id, text="Barcha kanallarga a'zo bo'lingan✅")
        await bot.send_message(chat_id=query.from_user.id, text="O'zingizga kerakli menyu orqali davom etishingiz mumkin:",
                               reply_markup=keyboardbutton(["Jamoa yaratish", "Jamoaga qo'shilish"]))
        await User_state.main_menu.set()
    else:
        await bot.answer_callback_query(query.id, text="Barcha kanallarga a'zo bo'linmagan❎")


dp.register_message_handler(cmd_start, content_types=[ct.TEXT])

"""
USERS APPS
"""

# main_menu

dp.register_message_handler(user.main_menu, content_types=[ct.TEXT], state=User_state.main_menu)

# second_menu

dp.register_message_handler(user.join_team, content_types=[ct.TEXT], state=User_state.join_team)
dp.register_message_handler(user.create_team, content_types=[ct.TEXT], state=User_state.create_team)
dp.register_message_handler(user.creator_pubg_id, content_types=[ct.TEXT], state=User_state.creator_pubg_id)
dp.register_message_handler(user.team_settings, content_types=[ct.TEXT], state=User_state.team_settings)
dp.register_message_handler(user.delete_team, content_types=[ct.TEXT], state=User_state.delete_team)
dp.register_message_handler(user.team_pubgers, content_types=[ct.TEXT], state=User_state.team_pubgers)
dp.register_message_handler(user.pubger, content_types=[ct.TEXT], state=User_state.pubger)
dp.register_message_handler(user.join_team_pubg_id, content_types=[ct.TEXT], state=User_state.join_team_pubg_id)
dp.register_message_handler(user.join_team_pubger_name, content_types=[ct.TEXT], state=User_state.join_team_pubger_name)
dp.register_message_handler(user.pubger_menu, content_types=[ct.TEXT], state=User_state.pubger_menu)

#
# """
# ADMIN APPS
# """
#
# # main_menu
#
# dp.register_message_handler(admin.main_menu, content_types=[ct.TEXT], state=Admin_state.main_menu)
#
# # second_menu
#
# dp.register_message_handler(admin.second_menu, content_types=[ct.TEXT], state=Admin_state.second_menu)
#
# # third_menu
#
# dp.register_message_handler(admin.third_menu, content_types=[ct.TEXT], state=Admin_state.third_menu)
#
# # fourth menu
#
# dp.register_message_handler(admin.fourth_menu, content_types=[ct.TEXT], state=Admin_state.fourth_menu)
#
# # add third menu
#
# dp.register_message_handler(admin.add_new_media_type, content_types=[ct.TEXT], state=Admin_state.add_new_media_type)
#
# # add second menu
#
# dp.register_message_handler(admin.add_new_day, content_types=[ct.TEXT], state=Admin_state.add_new_day)
#
# # add new media
#
# dp.register_message_handler(admin.add_new_media, content_types={ct.TEXT, ct.AUDIO, ct.PHOTO, ct.VIDEO, ct.VOICE,
#                                                                 ct.DOCUMENT}, state=Admin_state.add_new_media)
