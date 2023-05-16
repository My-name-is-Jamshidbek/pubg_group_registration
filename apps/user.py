"""
log in
"""
from aiogram.dispatcher import FSMContext as s
from aiogram.types import Message as m
from keyboardbutton import keyboardbutton
from loader import bot
from states import *
from database import database


async def main_menu(m: m):
    """
    :param m:
    :return:
    """
    textwrap = m.text
    if textwrap == "Jamoaga qo'shilish":
        await m.answer("Jamoa _id sini kiriting:",
                       reply_markup=keyboardbutton(["Jamoa yaratish"]))
        await User_state.join_team.set()
    elif textwrap == "Jamoa yaratish":
        await m.answer("Siz jamoa yaratishingiz bilan jamoa manageriga (admin) aylanasiz!\nJamoa uchun nom kiriting:",
                       reply_markup=keyboardbutton(["Jamoaga qo'shilish"]))
        await User_state.create_team.set()
    else:
        await m.answer("Bunday menyu mavjud emas!", reply_markup=keyboardbutton(["Jamoa yaratish",
                                                                                 "Jamoaga qo'shilish"]))


async def join_team(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    if textwrap == "Jamoa yaratish":
        await m.answer("Siz jamoa yaratishingiz bilan jamoa manageriga (admin) aylanasiz!\nJamoa uchun nom kiriting:",
                       reply_markup=keyboardbutton(["Jamoaga qo'shilish"]))
        await User_state.create_team.set()
    elif database.search_team(textwrap):
        if int(database.team_member_count(team_id=textwrap)) < 7:
            await m.answer(f"{database.get_team_name(textwrap)} jamoasiga qo'shilish uchun PUBG _id ingizni kiriting:",
                           reply_markup=keyboardbutton(["Jamoani o'zgartirish"]))
            await state.update_data(team_id=textwrap)
            await User_state.join_team_pubg_id.set()
        else:
            await m.answer("Ushbu jamoa a'zolari soni maksimal miqdoriga yetgan!")
    else:
        await m.answer("Bu idga bog'liq jamoa topilmadi!")


async def join_team_pubg_id(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    if textwrap == "Jamoani o'zgartirish":
        await m.answer("Jamoa _id sini kiriting:",
                       reply_markup=keyboardbutton(["Jamoa yaratish"]))
        await User_state.join_team.set()
    else:
        await m.answer("To'liq ismingizni kiriting:")
        await state.update_data(pubg_id=textwrap)
        await User_state.join_team_pubger_name.set()


async def join_team_pubger_name(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    state_data = await state.get_data()
    if textwrap == "Jamoani o'zgartirish":
        await m.answer("Jamoa _id sini kiriting:",
                       reply_markup=keyboardbutton(["Jamoa yaratish"]))
        await User_state.join_team.set()
    else:
        database.add_pubger(name=textwrap, pubg_id=state_data.get("pubg_id"), team_id=state_data.get("team_id"))
        await m.answer("Jamoaga muvaffaqiyatli qo'shildingiz!\nJamoa nazorati:",
                       reply_markup=keyboardbutton(["Jamoa a'zolari", "Jamoa yaratuvchisi", "Jamoani tark etish"]))
        await state.update_data(pubger_name=textwrap)
        await User_state.pubger_menu.set()


async def pubger_menu(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    state_data = await state.get_data()
    if textwrap == "Jamoa a'zolari":
        await m.answer(f"Jamoa a'zolari:\n{database.get_team_pubgers(state_data.get('team_id'))}")
    elif textwrap == "Jamoani tark etish":
        database.out_team(state_data.get("team_id"), state_data.get("pubger_name"))
        await m.answer("Siz jamoani tark etdingiz!")
        await m.answer(f"Kerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(["Jamoaga qo'shilish", "Jamoa yaratish"]))
        await User_state.main_menu.set()


async def create_team(m: m, state: s):
    """
    :param state:
    :param m:
    :return:
    """
    textwrap = m.text
    if textwrap == "Jamoaga qo'shilish":
        await m.answer("Jamoa _id sini kiriting:",
                       reply_markup=keyboardbutton(["Jamoa yaratish"]))
        await User_state.join_team.set()
    else:
        adding = database.create_team(user_id=m.from_user.id, name=textwrap)
        if adding:
            await m.answer(f"Jamoa muvaffaqiyatli yaratildi!\nJamoangiz idsi: {adding}\nPUBG _id ingizni kiriting:",
                           reply_markup=keyboardbutton([
                               "Men o'yinda ishtirok etmayman"]))
            await state.update_data(team_id=adding)
            await User_state.creator_pubg_id.set()
        else:
            await m.answer("Jamoa yaratishni iloji bo'lmadi!\nIltimos qayta urinib ko'ring:",
                           reply_markup=keyboardbutton(["Jamoaga qo'shilish"]))


async def creator_pubg_id(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    state_data = await state.get_data()
    if textwrap != "Men o'yinda ishtirok etmayman":
        if database.add_pubger(pubg_id=textwrap, team_id=state_data.get("team_id"), name='creator'):
            await m.answer("Muvaffaqiyatli qo'shildingiz.")
        else:
            await m.answer("Jamoaga qo'shilishni iloji bo'lmadi.")

    await m.answer("Jamoa nazorati:", reply_markup=keyboardbutton(["Jamoa a'zolari", "Jamoani o'chirish"]))
    await User_state.team_settings.set()


async def team_settings(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    state_data = await state.get_data()
    if textwrap == "Jamoani o'chirish":
        await m.answer("Haqiqatdan ham jamoangizni o'chirmoqchimisiz?", reply_markup=keyboardbutton(["Ha",
                                                                                                     "Bekor qilish"]))
        await User_state.delete_team.set()
    elif m.text == "Jamoa a'zolari":
        await m.answer("Jamoa a'zolari:",
                       reply_markup=keyboardbutton(database.team_pubgers(state_data.get("team_id")) + [
                           "Chiqish"]))
        await User_state.team_pubgers.set()
    else:
        await m.answer("Bunday menyu mavjud emas!")


async def delete_team(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    state_data = await state.get_data()
    if textwrap == "Ha":
        database.del_team(state_data.get("team_id"))
        await m.answer(f"Jamoa o'chirildi!Kerakli menyuni tanlashingiz mumkin:",
                       reply_markup=keyboardbutton(["Jamoaga qo'shilish", "Jamoa yaratish"]))
        await User_state.main_menu.set()
    else:
        await m.answer("Jamoa a'zolari:",
                       reply_markup=keyboardbutton(database.team_pubgers(state_data.get("team_id")) + [
                           "Chiqish"]))
        await User_state.team_pubgers.set()


async def team_pubgers(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    textwrap = m.text
    state_data = await state.get_data()
    if textwrap in database.team_pubgers(state_data.get("team_id")):
        await m.answer(database.team_pubger(state_data.get("team_id"), textwrap), reply_markup=keyboardbutton([
            "Jamoadan chetlatish", "Jamoa a'zolari"]))
        await state.update_data(pubger=textwrap)
        await User_state.pubger.set()
    elif m.text == "Chiqish":
        await m.answer("Jamoa nazorati:", reply_markup=keyboardbutton(["Jamoa a'zolari", "Jamoani o'chirish"]))
        await User_state.team_settings.set()
    else:
        await m.answer(f"{textwrap} nomli jamoa a'zosi mavjud emas!")


async def pubger(m: m, state: s):
    """
    :param m:
    :param state:
    :return:
    """
    state_data = await state.get_data()
    textwrap = m.text
    if textwrap == "Jamoa a'zolari":
        await m.answer("Jamoa a'zolari:",
                       reply_markup=keyboardbutton(database.team_pubgers(state_data.get("team_id")) + [
                           "Chiqish"]))
        await User_state.team_pubgers.set()
    elif textwrap == "Jamoadan chetlatish":
        database.del_pubger(state_data.get("team_id"), state_data.get("pubger"))
        await m.answer(f"{state_data.get('pubger')} jamoadan chetlatildi")
        await m.answer("Jamoa a'zolari:",
                       reply_markup=keyboardbutton(database.team_pubgers(state_data.get("team_id")) + [
                           "Chiqish"]))
        await User_state.team_pubgers.set()
    else:
        await m.answer("Bunday menyu mavjud emas!")
