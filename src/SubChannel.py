from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Callable, Dict, Any, Awaitable

from src import mysql

class SubChannel(BaseMiddleware):
    async def __call__(
            self, 
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
            event: Message, 
            data: Dict[str, Any]
    ):
        try:
            connection = mysql.create_connection()
            cursor = connection.cursor()    

            cursor.execute("SELECT * FROM channels")
            row = cursor.fetchall()
            st = False; i = 0

            if row:
                button = InlineKeyboardBuilder()
                for channel in row:
                    get = await event.bot.get_chat_member(chat_id=channel[1], user_id=event.chat.id)
                    if get.status not in ['creator', 'administrator', 'member']:
                        st = True; i += 1
                        set = await event.bot.get_chat(chat_id=channel[1])
                        button.button(text=f"{i} - Kanal", url=f"https://t.me/{set.username}")
                
                if st == True:
                    button.button(text="✅ Tekshirish", callback_data='check_channel')
                    button.adjust(1)
                    await event.answer(
                        text="✅ Botdan foydalanish uchun\n☺️Kanallarimizga obuna bo'ling!",
                        reply_markup=button.as_markup()
                    )
                else:
                    return await handler(event, data)
            else:
                return await handler(event, data)

        except:
            pass
        finally:
            cursor.close()
            connection.close()

