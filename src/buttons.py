from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

channel_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✨ SIRLI KINOLAR", url="t.me/sirli_kino")
        ]
    ]
)

admin_btn = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text="📽 Kinolar"
            )
        ],
        [
            KeyboardButton(text="✨ Kanal"),
            KeyboardButton(text="📊Hisobot")
        ],
        [
            KeyboardButton(text="💻Admin")
        ]
    ]
)

menu_1 = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="➕ Qo'shish"),
            KeyboardButton(text="➖ O'chirish")
        ],
        [
            KeyboardButton(text="❌ Bekor qilish")
        ]
    ]
)

yes_or_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✨ Ha", callback_data='yes'),
            InlineKeyboardButton(text="❌ Yo'q", callback_data='no')
        ]
    ]
)

remove_btn = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="❌ Bekor qilish")
        ]
    ]
)

link_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📥 YUKLAB OLISH", url="t.me/SirliKino_bot")
        ]
    ]
)

button_for_channel_menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="📃Ro'yxat")
        ],
        [
            KeyboardButton(text="➕Qo'shish"),
            KeyboardButton(text="➖O'chirish")
        ],
        [
            KeyboardButton(text="❌ Bekor qilish")
        ]
    ]
)

