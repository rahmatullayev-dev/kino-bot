from aiogram import Router, Bot, F
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.states import User
from src.SubChannel import SubChannel
from src import mysql

import json

from src import buttons, mysql

router = Router()
router.message.outer_middleware(SubChannel())

@router.message(Command(commands=['start']))
async def command_start(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(User.signIn)
    mysql.create_user(message.from_user.id)
    await message.reply(f"""☺️ <b>Assalomu aleykum,</b>\n\n📽 Bu yerda kino kodini kiritib yuklab qilishingiz mumkin.\n🎬 Maxsus kino kodlarini esa kino kanaldan topasiz.\n\n✅ Bot: @SirliKino_bot""", reply_markup=buttons.channel_btn, parse_mode="HTML")


@router.message(F.text.isnumeric())
async def send_movie(message: Message):
    data = mysql.get_movie(message.text)

    if data == None:
        await message.reply("😔 <b>Afsuski kino topilmadi!</b>", parse_mode="html")
    else:
        await message.answer_video(
            video=data[0][1],
            caption=f"☺️<b>Bizning botning nomi \"✨Sirli Kino bot\"\nshundan kelib chiqib kinolar nomi yashirilgan bo'ladi..\n\n🎲 Kino kodi: </b><i>{message.text}</i>\n<b>📥 Yulanish soni: </b><i>{data[0][2]} ta</i>",
            parse_mode="html",
            reply_markup=buttons.channel_btn
        )


@router.my_chat_member()
async def left_member(event: ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        mysql.enable_user(event.chat.id)
    elif event.new_chat_member.status == "kicked":
        mysql.disable_user(event.chat.id)


@router.callback_query()
async def check_channel(callback: CallbackQuery, bot: Bot):
    try:
        data = callback.data
        if data == "check_channel":
            connection = mysql.create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM channels")
            channels = cursor.fetchall()

            if channels:
                btn = InlineKeyboardBuilder()
                i=0; km = False
                for channel in channels:
                    i += 1
                    get = await bot.get_chat_member(
                        chat_id=channel[1],
                        user_id=callback.message.chat.id
                    )
                    data = await bot.get_chat(chat_id=channel[1])
                    if get.status not in ['administrator', 'creator', 'member']:
                        km = True
                        btn.button(
                            text=f"{i} - Kanal",
                            url=f"https://t.me/{data.username}"
                        )
                btn.button(
                    text="✅ Tekshirish",
                    callback_data='check_channel'
                )
                btn.adjust(1)
                if km:
                    await callback.answer(text="☺️ Hali kanallar mavjud") 
                    await callback.message.edit_text(
                        text="☺️ Hali kanallar mavjud",
                        inline_message_id=callback.inline_message_id,
                        reply_markup=btn.as_markup()
                    )
                else:
                    await callback.answer(text="✅ Obuna bo'ldingiz", show_alert=True, cache_time=1)
                    await callback.message.edit_text(
                        text="Siz kannalarga obuna bo'ldingiz!\nKino kodini kiriting..",
                        inline_message_id=callback.inline_message_id
                    )
            else:
                await callback.answer(text="✅ Obuna bo'ldingiz", show_alert=True, cache_time=1)
                await callback.message.edit_text(
                    text="Kanallarga obuna bo'ldingiz\nKino kodini kiriting..",
                    inline_message_id=callback.inline_message_id
                )
    except Exception as e:
        print(e) 
    finally:
        cursor.close()
        connection.close()
