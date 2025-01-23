from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src import buttons, states, mysql

admins = [7377998298]
kino_kanal = "@sirli_kino"

router = Router()

@router.message(F.text == "/panel")
async def command_panel(message: Message, state: FSMContext):
    state.clear
    if message.from_user.id in admins:
        await message.reply(
            text="<b>Xush kelibsiz admin!</b>",
            reply_markup=buttons.admin_btn,
            parse_mode="html"
        )

@router.message(F.text == "❌ Bekor qilish")
async def command_panel(message: Message, state: FSMContext):
    state.clear
    if message.from_user.id in admins:
        await message.reply(
            text="<b>Jarayon bekor qilindi!</b>",
            reply_markup=buttons.admin_btn,
            parse_mode="html"
        )


@router.message(F.text == "📊Hisobot")
async def hisobot(message: Message):
    try:
        connection = mysql.create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM data")
        data = cursor.fetchall()
        s = 0
        for i in data:
            s += 1
        bk=0; bs=0; count=0
        for user in users:
            count += 1
            if user[2] == 1:
                bk += 1
            else:
                bs += 1
        await message.reply(
            text=f"""<b>
📊Hisobot \n
👥Foydalanuvchilar:</b>
- Jami: {count} ta
- Bloklaganlar: {bk} ta
- Bloklamaganlar: {bs} ta \n
<b>🎥Kinolar:</b> {s} ta""",
            parse_mode="html"
        )
    except mysql.mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

# Channel

@router.message(F.text == "✨ Kanal")
async def reply_to_kanal(message: Message, state: FSMContext):
    await message.reply(
        text="✨ Majburiy obuna menyusi",
        reply_markup=buttons.button_for_channel_menu
    )
    await state.set_state(states.SubChannelState.signin)

@router.message(states.SubChannelState.signin, F.text == "➕Qo'shish")
async def channel_1(message: Message, state: FSMContext):
    await message.reply(
        text="Qo'shiladigan kanal id raqamini yoki usernamesi yuboring..",
        reply_markup=buttons.remove_btn
    )
    await state.set_state(states.SubChannelState.add)

@router.message(states.SubChannelState.signin, F.text == "➖O'chirish")
async def delete_channel(message: Message, state: FSMContext):
    await message.reply(
        text="O'chiriladigan kanal usernamesi yoki id raqamini yuboring"
    )
    await state.set_state(states.SubChannelState.remove)

@router.message(states.SubChannelState.signin, F.text == "📃Ro'yxat")
async def list_channel(message: Message, bot: Bot, state: FSMContext):
    try:
        data = mysql.all_channel()
        i = 0; matn = ''
        for channel in data:
            i += 1
            get = await bot.get_chat(chat_id=channel[1])
            title = get.title
            matn += f"<b><i>{i} - {title}</i></b>\n"
        await message.reply(
            text=f"<b>📃 Kanallar ro'yxati:</b>\n\n{matn}",
            parse_mode="html"
        )

    except Exception as e:
        print(e)

@router.message(states.SubChannelState.remove) 
async def remove_channel(message: Message, state: FSMContext):
    status = mysql.remove_channel(message.text)
    if status == False:
        await message.reply(
            text="Kanal topilmadi!",
            reply_markup=buttons.admin_btn
        )
    else:
        await message.reply(
            text="Kanal o'chirildi",
            reply_markup=buttons.admin_btn
        )
    await state.clear()

@router.message(states.SubChannelState.add)
async def channel_add(message: Message, bot: Bot, state: FSMContext):
    try:
        text = message.text

        if "@" in text or "-100" in text and text.replace('-', '').isnumeric() or "https://t.me/+" in text:
            res = mysql.add_channel(text)

            if res == False:
                await message.reply(
                    text="Kanal mavjud\nBoshqasini kiriting.."
                )
            else:
                await message.reply(
                    text="Kanal muvaffaqiyatli qo'shildi!",
                    reply_markup=buttons.admin_btn
                )
                await state.clear()
        else:
            await message.reply(
                text="Siz kanal manzilini kiritmadingiz..",
                reply_markup=buttons.admin_btn
            )
            await state.clear()
    except Exception as e:
        await state.clear()
        print(e)


# Movie 

@router.message(F.text == "📽 Kinolar")
async def menu_kinolar(message: Message, state: FSMContext):
    await message.reply(
        text="<b>📽 Kinolar bo'limi.</b>",
        reply_markup=buttons.menu_1,
        parse_mode="html"
    )
    await state.set_state(states.Admin.movie)

@router.message(states.Admin.movie)
async def movie_page(message: Message, state: FSMContext):
    if message.text == "➕ Qo'shish":
        await message.reply("Kino faylini yuboring..", reply_markup=buttons.remove_btn)
        await state.set_state(states.Admin.addMovie)
    elif message.text == "➖ O'chirish":
        await message.reply("Kino kodini kiriting..", reply_markup=buttons.remove_btn)
        await state.set_state(states.Admin.delMovie)

@router.message(states.Admin.addMovie, F.video)
async def add_movie(message: Message, state: FSMContext):
    res = mysql.add_movie(message.video.file_id)
    if res == False:
        await message.reply("Ushbu kino oldin qo'shilgan..")
    else:
        await state.set_data({
            'file_id': res
        })
        await message.reply("Kino qabul qilindi..\nKino uchun rasm yoki video yuboring")
        await state.set_state(states.Admin.addMovie2)

@router.message(states.Admin.addMovie2)
async def callback_checker(message: Message, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if message.video:
        file_id = message.video.file_id
        await bot.send_video(
            chat_id=kino_kanal,
            video=file_id,
            caption=f"🎬 <b>Ushbu videoni kinosi botimizga joylandi, bot orqali kinoni yuklab olishingiz mumkin!\n\n🔢 Kino kodi:</b><i> {data.get("file_id")}</i>\n\n🤖<b> Bot manzili: @SirliKino_bot</b>",
            parse_mode="html",
            reply_markup=buttons.link_btn
        )
    elif message.photo:
        file_id = message.photo[0].file_id
        await bot.send_photo(
            chat_id=kino_kanal,
            photo=file_id,
            caption=f"🎬 <b>Ushbu rasmdagi kino botimizga joylandi, bot orqali kinoni yuklab olishingiz mumkin!\n\n🔢 Kino kodi:</b><i> {data.get("file_id")}</i>\n\n🤖<b> Bot manzili: @SirliKino_bot</b>",
            parse_mode="html",
            reply_markup=buttons.link_btn
        )
    
    await message.answer("Kino kanalga yuborildi!", reply_markup=buttons.admin_btn)
    
    await state.clear()

@router.message(states.Admin.delMovie, F.text.isnumeric())
async def delete_movie(message: Message, state: FSMContext):
    mysql.delete_movie(message.text)
    await message.answer("Ma'lumot tozalandi", reply_markup=buttons.admin_btn)
    await state.set_state(states.Admin.movie)

