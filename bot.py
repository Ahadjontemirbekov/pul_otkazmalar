import threading

from telegram.ext import CallbackQueryHandler, ConversationHandler, CallbackContext
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, \
    BotCommand, Update
import time
from PIL import Image, ImageDraw, ImageFont
import random
from telegram import Bot
import logging
import sqlite3
from datetime import datetime, date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from functools import wraps

games = {}
REKLAMA_XABAR = 0
REKLAMA_VAQT = 1

captchani_soni = 0

rasm_raqam = 1
con = sqlite3.connect('hisoblar.db')
cur = con.cursor()
CHANNEL_USERNAME = "@pul_hisoblari"

kunlik_salomlar = {
    0: """🌞 *Dushanba* – Yangi hafta, yangi imkoniyatlar! ✨💼

Bugun yangi maqsadlar sari qadam qo‘yish va orzular sari intilish uchun eng yaxshi kun! 💪
Hayot senga imkoniyatlar eshigini ochmoqda – sen esa bu eshikdan bemalol kirib borishing kerak. 🚪🌈
Kechagi xatolaring – bu darslik. Ularni unut, ammo o‘rgan! 📘❌
Bugun harakat, mehnat, ishonch va intilish kuni. 🚀🛠️

Unutma, eng katta yutuqlar eng oddiy harakatlar bilan boshlanadi. 📈
Bugun o‘zingni isbotlash kuni. Sen har qanday to‘siqdan o‘ta oladigan kuchga egasan. 🔥🧠
Bugungi dushanba – bu yangi sahifa, yangi imkoniyat. Bor kuchingni yig‘ va boshlang! 📝🏁""",

    1: """🚀 *Seshanba* – Vaqt to‘xtamaydi, hayot esa harakatni sevadi! ⏳🔄

Bugun – rejalaringni bir qadam yaqinlashtiradigan kun. 🧭
Kecha boshlangan ishingni davom ettir, yanada ilgarila. 🛤️💼
Sabr, qat’iyat va mehnat seni istagan cho‘qqinga olib boradi. 🧗‍♂️🏔️

Bugun sen ilhom topishing, fikrlaringni tartibga solishing va yangi rejalar tuzishing mumkin. 🧠🗂️
Hech qachon imkonni boy bermang – bu kun hayotingizni o‘zgartirishi mumkin. ✨🎯
Motivatsiya doimo ichingda! Uni uyg‘ot va harakatda bo‘l! 🔋🔥""",

    2: """🌟 *Chorshanba* – Yo‘lning yarmi ortda qoldi! 🛣️👏

Sen allaqachon katta yo‘l bosib o‘tding, endi to‘xtab qolma! ⛔
Bugun ichki kuchingni his qil va ilhomlan! 🌠💡
O‘zingdan faxrlan, sen har kuni o‘zingni engib kelayapsan. 🏆💖

Bugun – ijod, kuch va tafakkur kuni. 🧘‍♂️🎨
Yashash – bu ilhom olish va boshqalarga ilhom berish. 💬❤️
Bugun eng yaxshi versiyangni ochib ber – sen bunga loyiqsan! ✅🌈""",

    3: """🌈 *Payshanba* – Kelajak bugundan boshlanadi! 📅🕰️

Bugungi mehnating – ertangi yutuqlaring poydevori. 🧱🏗️
O‘zingga ishon, orzularingga sodiq bo‘l, harakatni to‘xtatma. 💖🛤️
Sabrli bo‘l, har bir qadam – bu yutuqqa yo‘l! 🪜🏁

Bugun yangi g‘oyalar tug‘ilishi mumkin – ularga quloq sol! 🎧🌱
O‘zingni yengil his qil, atrofingdagi go‘zallikni ko‘r. 🌺🕊️
Yaxshi so‘z, yaxshi niyat – ularga to‘yingan kun bo‘lsin. 💬🙏""",

    4: """💥 *Juma* – Haftaning eng kuchli kunlaridan biri! 🎉📆

Bugungi kun – rejalaringni yakunlash, muvaffaqiyat sari nuqta qo‘yish uchun imkon. ✅🖋️
Oldingdagi yo‘ldan mamnun bo‘l – sen harakat qilding, endi baraka kut. 🌾
Bugun – barakali yakun, xotirjam yurak, va orzular sari yangi rejalar kuni. 💡📈

Tinchlik, hushyorlik va ilhom bugun sen bilan bo‘lsin. 🕊️🧘
Haqiqiy mehnat – oxirida zavq beradi. Sen bunga loyiqsan. 🥇💫
Bugun o‘zingni mukofotla – sen zo‘rsan! 🛍️🍫""",

    5: """🎉 *Shanba* – Yay! Dam olish kuni! ☕📖

Bugun – ichki kuchni tiklash, yaqinlar bilan vaqt o‘tkazish, o‘zingni eslash kuni. 🛌💬
Kitob o‘qi, film ko‘r, yur, dam ol – bugun yuragingni tingla. 🎥📚🚶‍♂️
Yuragingdagi orzularni yana bir bor esla va ilhomlan. 🌟📝

Oddiylikdagi go‘zallikni ko‘r. 🍂🎈
Bugun yangi g‘oyalar, go‘zal kayfiyat va tinchlik senga yor bo‘lsin. 🕊️💖
Sen bugun eng muhim odamsan – o‘zingga vaqt ajrat! 🪞🧴""",

    6: """🧘 *Yakshanba* – Tinchlik, xotirjamlik va tafakkur kuni. 🌿📖

Bugun o‘tgan haftani tahlil qil, o‘zingni tingla, ichki ovozingga quloq sol. 🧠👂
Dam ol, o‘yla, rejala. Yangi haftani qanday boshlashni his et. 📆🗒️
Shukr qil – bugungi kuning bor, imkoning bor. 🤲💖

Bugun – yuragingni tozalash, ruhingni yengillashtirish, yangi orzularni tug‘dirish kuni. 💭🌄
Sokin musiqa, iliq choy va ijobiy kayfiyat bilan to‘yingan yakshanba bo‘lsin. 🎶🍵😊
Ertaga eng yaxshi haftani boshlash uchun kuch yig‘ – sen bunga tayyorsan! 🏋️‍♂️⚡"""
}

admin_menyu = [
    [KeyboardButton('Botga start bosganlar 📝')],
    [KeyboardButton("Botdan ro'yxatdan o'tganlar  👤"), KeyboardButton("Adminga berilgan savollar 📝")],
    [KeyboardButton("Foydalanuvchini bloklash 🚫"), KeyboardButton("Adminlik huquqini berish 🤝")],
    [KeyboardButton("Foydalanuvchini blokdan chiqarish 🫸🏻"), KeyboardButton("Adminlik huquqini olish ☠️")],
    [KeyboardButton("Blockdagilarni ko'rish 👀"), KeyboardButton("Adminlarni ko'rish 👀")],
    [KeyboardButton("🌿✨ Reklama berish ❤️😜📸")],

]

bosh_menyu = [
    [KeyboardButton(text="Kartaga pul qo'shish 💳"), KeyboardButton(text="Kartadan pul yechish 💰")],
    [KeyboardButton(text="Kartadan kartaga pul o'tgazish  💳  🔜  🪪"),
     KeyboardButton(text="Kartadagi pulni ko'rish 💰")],
    [KeyboardButton(text="Admin bilan bog'lanish ☘️"), KeyboardButton(text="Boshiga qaytish👑 ⬅️")],
    [KeyboardButton(text="Savol berish 🪐"), KeyboardButton(text="Ro'yxatdan o'tganlarni ko'rish 📋")],
    [KeyboardButton(text="💫 Allohning 99ta ismlari ✨"), KeyboardButton(text="Profil uchun rasmlar 👑")],
    [KeyboardButton(text="⚙️ Sozlamalar"), KeyboardButton(text="Yon daftar 📝")],
    [KeyboardButton(text="😜 Adminga savol berish ✨"), KeyboardButton(text="Kanal ✨")],
    [KeyboardButton(text="🎧 My music 🖤"), KeyboardButton(text="📖 Kitoblar ✨")],
    [KeyboardButton(text="👑 Islomiy multfilimlar 🎞")],
    [KeyboardButton(text="SMS ✉️ yuborish"), KeyboardButton(text="O'yinlar 🎮")],
    [KeyboardButton(text="Mening profilim ⚡️")],
]

user_ids = set()


def create_math_image():
    a = random.randint(10, 99)
    b = random.randint(10, 99)
    misol = f"{a} + {b} = ?"
    javob = a + b

    width, height = 400, 200
    bg_color = (random.randint(150,255), random.randint(150,255), random.randint(150,255))
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # 📌 Chiziqlar chizamiz
    for _ in range(25):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        draw.line((x1, y1, x2, y2), fill=color, width=1)

    # ✅ Shrift yuklash (agar Arial bo‘lmasa, default ishlatiladi)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf", 50)
    except OSError:
        font = ImageFont.load_default()

    # 📌 Matn markazga joylashtiriladi
    bbox = draw.textbbox((0, 0), misol, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (width - text_w) // 2
    text_y = (height - text_h) // 2

    draw.text((text_x, text_y), misol, fill=(0, 0, 0), font=font)

    # 📌 Rasmni saqlash
    image.save("captcha.png")
    return "captcha.png", javob


def xato_captcha(update, context):
    file, ans = create_math_image()
    x1 = random.randint(10, 99)
    x2 = random.randint(10, 99)
    x3 = random.randint(10, 99)

    context.user_data["true"] = f"Javob {ans}"
    context.user_data["x1"] = f"Javob {x1}"
    context.user_data["x2"] = f"Javob {x2}"
    context.user_data["x3"] = f"Javob {x3}"
    button = [
        KeyboardButton(f"Javob {x1}"),
        KeyboardButton(f"Javob {ans}"),
        KeyboardButton(f"Javob {x2}"),
        KeyboardButton(f"Javob {x3}"),
    ]

    random.shuffle(button)

    photo = open(file, 'rb')

    reply_markup = ReplyKeyboardMarkup([button], resize_keyboard=True)

    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=photo,
                           caption="Botdan foydalanish uchun avval misolni yeching:",
                           reply_markup=reply_markup
                           )


def captcha(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        if captchani_soni == 1:
            return func(update, context, *args, **kwargs)
        filename, javob = create_math_image()
        x1 = random.randint(10, 99)
        x2 = random.randint(10, 99)
        x3 = random.randint(10, 99)

        context.user_data["true"] = f"Javob {javob}"
        context.user_data["x1"] = f"Javob {x1}"
        context.user_data["x2"] = f"Javob {x2}"
        context.user_data["x3"] = f"Javob {x3}"
        button = [
            KeyboardButton(f"Javob {x1}"),
            KeyboardButton(f"Javob {javob}"),
            KeyboardButton(f"Javob {x2}"),
            KeyboardButton(f"Javob {x3}"),
        ]

        random.shuffle(button)

        photo = open(filename, 'rb')

        reply_markup = ReplyKeyboardMarkup([button], resize_keyboard=True)

        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=photo,
                               caption="Botdan foydalanish uchun avval misolni yeching:",
                               reply_markup=reply_markup
                               )
        return "TANLA"

    return wrapper


def block(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id

        con = sqlite3.connect('hisoblar.db')
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS bloclar (
            id INTEGER
        );
        """)
        cur.execute("SELECT id FROM bloclar WHERE id = ?", (user_id,))
        is_blocked = cur.fetchone()
        con.close()

        if is_blocked:
            update.message.reply_text("❌")
            update.message.reply_text("❌ Siz ahadjon tomonidan blocklangansiz. ")
            return

        return func(update, context, *args, **kwargs)

    return wrapper


def adm(func):
    @wraps(func)
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.effective_user.id

        con = sqlite3.connect('hisoblar.db')
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS adminlar (
            id INTEGER
        );
        """)
        cur.execute("SELECT id FROM adminlar WHERE id = ?", (user_id,))
        is_admin = cur.fetchone()
        con.close()

        if not is_admin:
            update.message.reply_text("🤌🏻")
            update.message.reply_text("Siz admin emassiz 🤌🏻")
            return

        return func(update, context, *args, **kwargs)

    return wrapper


@captcha
@block
def start(update, context):
    time.time()

    user_id = update.message.chat_id
    user_ids.add(user_id)
    ####################################################
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    print(first_name)
    last_name = update.message.from_user.last_name
    user_name = update.message.from_user.username
    vaqt = datetime.now()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS start_bosganlar (
        id INTEGER,
        first_name TEXT,
        last_name TEXT,
        user_name TEXT,
        vaqt TEXT
    );
    """)
    cur.execute(
        "INSERT INTO start_bosganlar (id, first_name, last_name, user_name, vaqt) VALUES (?, ?, ?, ?, ?)",
        (id, first_name, last_name, user_name, vaqt)
    )
    con.commit()
    context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=f"""
        🆔 ID: {id}
        👤 Ismi: {first_name}
        👥 Familiyasi: {last_name}
        💬 Username: @{user_name}
        ⏰ Vaqt: {vaqt}

        botimga start bosdi
        👍
        """
    )

    #########################################

    cur.execute("SELECT id FROM users WHERE id=?;", (id,))
    natijalar = cur.fetchone()
    topildi = False
    try:
        for row in natijalar:
            if row == id:
                topildi = True
                break
    except:
        k = [
            [KeyboardButton(text="Kirish ✅"), KeyboardButton(text="Ro'yxatdan o'tish 📜")]
        ]
        update.message.reply_text("😁")
        update.message.reply_text(text=
                                  "🍃 💫 Assalomu alaykum ☘️✨\n\n"
                                  f"🤖 Botimga xush kelibsiz {first_name} 👤💫 Bu bot odamlar uchun foydali bo‘lsa, men juda xursand bo‘lardim 😊🥰\n\n"
                                  "🤖 Bot qanday ishlaydi:\n\n⭕️ Bot ishlashi uchun avval Ro'yxatdan o'tish 📜 tugmasini bosib Ro'yxatdan o'ting \n\n"
                                  "❗️ Agar Ro'yxatdan o'tgan bo'lsangiz Kirish ✅ tugmasini bosib korishingiz mumkin 👌🏻\n\n"
                                  "💫 Bu bot odamlar uchun foydali bo‘lsa, men juda xursand bo‘lardim 😊🥰\n\n"
                                  "👑 Botimizdan bemalol foydalanishingiz mumkin 😇\n\n"
                                  "⭕️ Agar botimda biror kamchilik bo‘lsa  @Ahadjon_tem1rbekov 👤, bemalol aytishingiz mumkin 🧏🏻‍♀️\n\n"
                                  "📜 Bundan men juda xursand bo‘laman 🙃\n\n"
                                  "📌 Masalan: Botning bu yerida xato bor, bunday qilinsa bu chiqyapti, aslida esa bu chiqishi kerak\n\n"
                                  "Yoki bu yerda imloviy xato bor, shunday bo‘lishi kerak va shunga o‘xshash\n\n"
                                  "📋 Bu ish hammamiz uchun foydali bo‘ladi va savob ham olib keladi 🕋\n\n"
                                  "🔹 Asosiy Buyruqlar:\n/start - Botni ishga tushirish\n/help - Botdan foydalanish qo'llanmasi\n/menyu - Buyruqlar\n\n"
                                  "❗️ Eslatma: \nBotdan to'liq foydalanish uchun avval ro'yxatdan o'tishingiz kerak!\n\n"
                                  "💫 Murojaat uchun: ✨ @Ahadjon_tem1rbekov 👤"
                                  )
        update.message.reply_text(text="*🍃 💫 Assalomu alaylum  ☘️✨*", parse_mode="Markdown",
                                  reply_markup=ReplyKeyboardMarkup(k, one_time_keyboard=True, resize_keyboard=True))
        return "TANLA"

    if topildi:
        update.message.reply_text("😁")
        update.message.reply_text(text=
                                  "🍃 💫 Assalomu alaykum ☘️✨\n\n"
                                  f"🤖 Botimga xush kelibsiz {first_name} 👤💫 Bu bot odamlar uchun foydali bo‘lsa, men juda xursand bo‘lardim 😊🥰\n\n"
                                  "🤖 Bot qanday ishlaydi:\n\n⭕️ Bot ishlashi uchun avval Ro'yxatdan o'tish 📜 tugmasini bosib Ro'yxatdan o'ting \n\n"
                                  "❗️ Agar Ro'yxatdan o'tgan bo'lsangiz Kirish ✅ tugmasini bosib korishingiz mumkin 👌🏻\n\n"
                                  "💫 Bu bot odamlar uchun foydali bo‘lsa, men juda xursand bo‘lardim 😊🥰\n\n"
                                  "👑 Botimizdan bemalol foydalanishingiz mumkin 😇\n\n"
                                  "⭕️ Agar botimda biror kamchilik bo‘lsa  @Ahadjon_tem1rbekov 👤, bemalol aytishingiz mumkin 🧏🏻‍♀️\n\n"
                                  "📜 Bundan men juda xursand bo‘laman 🙃\n\n"
                                  "📌 Masalan: Botning bu yerida xato bor, bunday qilinsa bu chiqyapti, aslida esa bu chiqishi kerak\n\n"
                                  "Yoki bu yerda imloviy xato bor, shunday bo‘lishi kerak va shunga o‘xshash\n\n"
                                  "📋 Bu ish hammamiz uchun foydali bo‘ladi va savob ham olib keladi 🕋\n\n"
                                  "🔹 Asosiy Buyruqlar:\n/start - Botni ishga tushirish\n/help - Botdan foydalanish qo'llanmasi\n/menyu - Buyruqlar\n\n"
                                  "❗️ Eslatma: \nBotdan to'liq foydalanish uchun avval ro'yxatdan o'tishingiz kerak!\n\n"
                                  "💫 Murojaat uchun: ✨ @Ahadjon_tem1rbekov 👤"
                                  )
        cur.execute("SELECT ism FROM users WHERE id=?;", (id,))
        natijalar = cur.fetchone()
        for f_ism in natijalar:
            update.message.reply_text(
                f"🥶 Siz ro'yxatdan o'tgansiz 🤪\n\nFoydalanuvchi 👤 ismi {f_ism} \n\n*☘️ Asosiy menyu ✨*",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(bosh_menyu, one_time_keyboard=False, resize_keyboard=True))
        return "TANLA"

    con.commit()
    cur.close()
    con.close()


@captcha
@block
def ism(update, context):
    ism = update.message.text
    con = sqlite3.connect("hisoblar.db")
    cur = con.cursor()
    cur.execute("SELECT ism FROM users")  # bazadagi ismlar ham kichik holatda olinadi
    natijalar = cur.fetchall()
    topildi = False
    for row in natijalar:
        if row[0] == ism:
            topildi = True
            break
    if topildi:
        update.message.reply_text("Uzur, bunday foydalanuvchi mavjud. ✅\n\nBoshqa ism kiriting 😉")
        update.message.reply_text("Foydalanuvchi 👤 ismi ")
        return "ISM"
    else:
        context.user_data['ism'] = update.message.text  # foydalanuvchi yozgan asl ism
        update.message.reply_text("*Raxmat 🙃 💫*", parse_mode="Markdown")
        update.message.reply_text("Familya 👤", parse_mode="Markdown")
        return "FAMILYA"


@captcha
@block
def familya(update, context):
    context.user_data['familya'] = update.message.text
    update.message.reply_text('*Raxmat 🙃 💫*', parse_mode="Markdown")
    update.message.reply_text('yosh 📆', parse_mode="Markdown")
    return "YOSH"


@captcha
@block
def yosh(update, context):
    context.user_data['yosh'] = update.message.text
    update.message.reply_text('*Raxmat 🙃 💫*', parse_mode="Markdown")
    k = [[KeyboardButton(text="Telefon raqamni yuborish ☎️", request_contact=True)]]
    update.message.reply_text('Telefon raqam 📞', parse_mode="Markdown",
                              reply_markup=ReplyKeyboardMarkup(k, one_time_keyboard=True, resize_keyboard=True))
    return "TELEFON_RAQAM"


@captcha
@block
def telefon_raqam(update, context):
    contact = update.message.contact
    if contact and contact.phone_number:
        context.user_data['telefon_raqam'] = contact.phone_number
        update.message.reply_text('*Raxmat 🙃 💫*', parse_mode="Markdown")
        update.message.reply_text(
            '*Parol kiriting 🔒*\n\n_Faqat esizda qolsin ⭕️_',
            parse_mode="Markdown"
        )
        return "PAROL"
    else:
        update.message.reply_text(
            'Iltimos, kontaktni tugma orqali yuboring 📱'
        )
        return "TELEFON"


@captcha
@block
def parol(update, context):
    context.user_data['parol'] = update.message.text
    update.message.reply_text('*Raxmat 🙃 💫*', parse_mode="Markdown")
    update.message.reply_text('_Qancha pul qoymoqchisiz_', parse_mode="Markdown")
    return "PUL"


@captcha
@block
def pul(update, context):
    context.user_data['pul'] = update.message.text
    update.message.reply_text('*Raxmat 🙃 💫 *\n\n_Malumotlar saqlandi 🗂_', parse_mode="Markdown")

    update.message.reply_text("*☘️ Asosiy menyu ✨*", parse_mode="Markdown",
                              reply_markup=ReplyKeyboardMarkup(bosh_menyu, one_time_keyboard=False,
                                                               resize_keyboard=True))

    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    user_name = update.message.from_user.username
    vaqt = datetime.now()
    ism = context.user_data['ism']
    familya = context.user_data['familya']
    yosh = context.user_data['yosh']
    telefon_raqam = context.user_data['telefon_raqam']
    parol = context.user_data['parol']
    pul = context.user_data['pul']

    # Jadval yaratish
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        first_name TEXT,
        last_name TEXT,
        user_name TEXT,
        vaqt TEXT,
        ism TEXT,
        familya TEXT,
        yosh INTEGER,
        telefon_raqam INTEGER,
        parol BLOB,
        pul INTEGER
    );
    """)
    cur.execute(
        "INSERT INTO users (id, first_name, last_name, user_name, vaqt,ism,familya,yosh,telefon_raqam,parol,pul) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (id, first_name, last_name, user_name, vaqt, ism, familya, yosh, telefon_raqam, parol, pul)
    )
    yashirin_telefon_raqam = f"{telefon_raqam[0]}{telefon_raqam[1]}{telefon_raqam[2]}{telefon_raqam[3]} {telefon_raqam[4]}{telefon_raqam[5]} XXX XX {telefon_raqam[-2]}{telefon_raqam[-1]}"
    context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=f"""
        🆔 ID: {id}
        👤 Ismi: {first_name}
        👥 Familiyasi: {last_name}
        💬 Username: @{user_name}
        ⏰ Vaqt: {vaqt}

        👤 To'liq ism: {ism} 🪐
        👤 To'liq familya: {familya} ⚡️
        👤 To'liq yosh: {yosh} 📆
        👤 To'liq telefon raqam: {yashirin_telefon_raqam} 📞
        👤 To'liq parol: XXXXXXX 🔒
        👤 To'liq pul: {pul} 💰

        botimdan ro'yxatdan o'tdi
        👍
        """
    )
    con.commit()
    cur.close()
    con.close()

    return "TANLA"


@captcha
@block
def clear(update, context):
    update.message.reply_text('*Raxmat 🙃 💫*', parse_mode="Markdown")
    return ConversationHandler.END


@captcha
@adm
@block
def bocklash_id(update, context):
    if update.message.text.isdigit():
        con = sqlite3.connect('hisoblar.db')
        cur = con.cursor()
        cur.execute(
            "INSERT INTO bloclar (id) VALUES (?)",
            (update.message.text,)
        )
        con.commit()
        update.message.reply_text("Foydalanuvchi blocklandi 🚫")
        return "TANLA"
    else:
        update.message.reply_text("Iltimos faqat son yuboring")


@adm
@block
def adminlik_id(update, context):
    if update.message.text.isdigit():
        con = sqlite3.connect('hisoblar.db')
        cur = con.cursor()
        cur.execute(
            "INSERT INTO adminlar (id) VALUES (?)",
            (update.message.text,)
        )
        con.commit()
        update.message.reply_text("Adminlik berildi")
        return "TANLA"
    else:
        update.message.reply_text("Iltimos faqat son yuboring")


@captcha
@block
def kiruvchi_ism(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute(f"SELECT ism FROM users WHERE ism='{text}';")
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['Foydalanuvchi_ismi'] = text
                update.message.reply_text(text="Foydalanuvchi 👤 topildi  raxmat ✅")
                update.message.reply_text(text="Parolni kiriting 🔐")
                return "KIRUVCHI_PAROL"
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def kiruvchi_parol(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute(f"SELECT parol FROM users WHERE parol='{text}';")
        n = cur.fetchone()
        for i in n:
            if text == i:
                update.message.reply_text("Raxmat ✅")
                update.message.reply_text("☘️ Asosiy menyu ✨", parse_mode="Markdown",
                                          reply_markup=ReplyKeyboardMarkup(bosh_menyu, one_time_keyboard=False,
                                                                           resize_keyboard=True))
                return "TANLA"
    except:
        update.message.reply_text(text="Parol xato kiritildi ❌ 👤")



@block
def yorilgan_xabar(update, context):
    text = update.message.text
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()

    cur.execute("SELECT id FROM bloclar ;")
    blocklar = cur.fetchall()

    id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    print(first_name)
    last_name = update.message.from_user.last_name
    user_name = update.message.from_user.username
    vaqt = datetime.now()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS yorilgan_xabar (
        id INTEGER,
        first_name TEXT,
        last_name TEXT,
        user_name TEXT,
        vaqt TEXT,
        yorilgan_xabar TEXT
    );
    """)
    cur.execute(
        "INSERT INTO yorilgan_xabar (id, first_name, last_name, user_name, vaqt,yorilgan_xabar) VALUES (?,?, ?, ?, ?, ?)",
        (id, first_name, last_name, user_name, vaqt, text)
    )
    con.commit()
    cur.close()
    con.close()

    if text == "Kirish ✅":
        update.message.reply_text(text='Foydalanuvchi 👤 ismi ')
        return "KIRUVCHI_ISM"
    elif text == "💫 Bosh sahifaga maytmayman ❌":
        update.message.reply_text(text='Siz boshiga qaymadingiz\n\nmenyulardan foydalanishingiz mumkin ',
                                  reply_markup=ReplyKeyboardMarkup(bosh_menyu, resize_keyboard=True))
        return "TANLA"

    elif text == "Ro'yxatdan o'tish 📜":
        update.message.reply_text(text="Foydalanuvchi 👤 ismi ")
        return "ISM"
    elif text == "Kanal ✨":
        k = [
            [InlineKeyboardButton(text="Kanal ✅", url="https://t.me/pul_hisoblari")]
        ]
        update.message.reply_text("🌿 Assalomu alaykum ✨", reply_markup=InlineKeyboardMarkup(k))
        return "TANLA"
    elif text == "O'yinlar 🎮":
        keyboard = [
            [InlineKeyboardButton("🔫", web_app={"url": "https://krunker.io/"})],
            [InlineKeyboardButton("🏎", web_app={"url": "https://slowroads.io/#A2-b220e4d5@2.99"})],
            # [InlineKeyboardButton("oyin", web_app={"url": "https://t.me/spinthe_bot/bottle"})],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "O'yinlarni o'ynashiz mumkin",
            reply_markup=reply_markup
        )

    elif text == "Yon daftar 📝":
        update.message.reply_text(text="Foydalanuvchi 👤 ismi ")
        return "Yon_daftar_ism"

    elif text == "Foydalanuvchini bloklash 🚫":
        update.message.reply_text(text="Blocklamoqchi bolgan foydalanuvchi 👤 telegram id si: ")
        return "bocklash_id"

    elif text == "Blockdagilarni ko'rish 👀":
        con = sqlite3.connect("hisoblar.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM bloclar ;")
        blocklar = cur.fetchall()
        if not blocklar:
            update.message.reply_text("Blocklanganlar yo'q")
        else:
            for i in blocklar:
                update.message.reply_text(i[0])
        return "TANLA"

    elif text == "Adminlarni ko'rish 👀":
        con = sqlite3.connect("hisoblar.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM adminlar ;")
        blocklar = cur.fetchall()
        if not blocklar:
            update.message.reply_text("Adminlar yo'q")
        else:
            for i in blocklar:
                update.message.reply_text(i[0])
        return "TANLA"

    elif text == "Adminlik huquqini berish 🤝":
        update.message.reply_text(text="Adminlik huquqini bermoqchi bolgan foydalanuvchi 👤 telegram id si: ")
        return "adminlik_id"

    elif text == "🌿✨ Reklama berish ❤️😜📸":
        update.message.reply_text("Reklama matnini yuboring ✍️")
        return "REKLAMA_XABAR"


    elif text.isdigit():
        con = sqlite3.connect("hisoblar.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM bloclar WHERE id =?", (text,))
        blocklar = cur.fetchall()

        if blocklar:
            cur.execute("DELETE FROM bloclar WHERE id=?", (text,))
            con.commit()
            update.message.reply_text('Foydalanuvchi blockdan chiqarildi🫷🏻 ',
                                      reply_markup=(ReplyKeyboardMarkup(admin_menyu, resize_keyboard=True)))
        else:
            cur.execute("DELETE FROM adminlar WHERE id=?", (text,))
            con.commit()
            update.message.reply_text('Foydalanuvchi adminlik huquqidan chiqarildi🫷🏻 ',
                                      reply_markup=(ReplyKeyboardMarkup(admin_menyu, resize_keyboard=True)))


    elif text == "Foydalanuvchini blokdan chiqarish 🫸🏻":
        con = sqlite3.connect("hisoblar.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM bloclar")
        users = [row[0] for row in cur.fetchall()]
        con.close()

        keyboard = [[user] for user in users]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text("Foydalanuvchini tanlang:", reply_markup=markup)

        return "TANLA"



    elif text == "Adminlik huquqini olish ☠️":
        con = sqlite3.connect("hisoblar.db")
        cur = con.cursor()
        cur.execute("SELECT id FROM adminlar")
        users = [row[0] for row in cur.fetchall()]
        con.close()

        keyboard = [[user] for user in users]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text("Foydalanuvchini tanlang:", reply_markup=markup)

        return "TANLA"



    elif text == "Botga start bosganlar 📝":
        con = sqlite3.connect('hisoblar.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM start_bosganlar ;")
        natijalar = cur.fetchall()
        for i in natijalar:
            update.message.reply_text(text=f"""
        Foydalanuvchi 👤 id : {i[0]}
        Foydalanuvchi 👤 first name : {i[1]}
        Foydalanuvchi 👤 last name : {i[2]}
        Foydalanuvchi 👤 user name : @{i[3]}
        Foydalanuvchi 👤 vaqt : {i[4]}
            """)
        return "TANLA"
    elif text == "Adminga berilgan savollar 📝":
        con = sqlite3.connect('hisoblar.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM adminga_Savol;")
        natijalar = cur.fetchall()
        for i in natijalar:
            update.message.reply_text(text=f"""
        Foydalanuvchi 👤 id : {i[0]}
        Foydalanuvchi 👤 first name : {i[1]}
        Foydalanuvchi 👤 last name : {i[2]}
        Foydalanuvchi 👤 user name : @{i[3]}
        Foydalanuvchi 👤 vaqt : {i[4]}
        Foydalanuvchi 👤 savol : {i[5]}
            """)
        return "TANLA"

    elif text == "Botdan ro'yxatdan o'tganlar  👤":
        con = sqlite3.connect('hisoblar.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM users;")
        natijalar = cur.fetchall()
        for i in natijalar:
            update.message.reply_text(text=f"""Foydalanuvchi 👤 id : {i[0]}
            Foydalanuvchi 👤 first name : {i[1]}
            Foydalanuvchi 👤 last name : {i[2]}
            Foydalanuvchi 👤 user name : @{i[3]}
            Foydalanuvchi 👤 vaqt : {i[4]}
            Foydalanuvchi 👤 ism : {i[5]}
            Foydalanuvchi 👤 familya : {i[6]}
            Foydalanuvchi 👤 yosh : {i[7]}
            Foydalanuvchi 👤 telefon raqam : +{i[8]}
            Foydalanuvchi 👤 parol : {i[9]}
            Foydalanuvchi 👤 pul : {i[10]}
            """)
        return "TANLA"

    elif text == "Mening profilim ⚡️":
        con = sqlite3.connect('hisoblar.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id=?;", (update.message.from_user.id,))
        natijalar = cur.fetchall()
        update.message.reply_text(text=f"""Foydalanuvchi 👤 id : {natijalar[0][0]}
        Foydalanuvchi 👤 first name : {natijalar[0][1]}
        Foydalanuvchi 👤 last name : {natijalar[0][2]}
        Foydalanuvchi 👤 user name : @{natijalar[0][3]}
        Foydalanuvchi 👤 vaqt : {natijalar[0][4]}
        Foydalanuvchi 👤 ism : {natijalar[0][5]}
        Foydalanuvchi 👤 familya : {natijalar[0][6]}
        Foydalanuvchi 👤 yosh : {natijalar[0][7]}
        Foydalanuvchi 👤 telefon raqam : +{natijalar[0][8]}
        Foydalanuvchi 👤 parol : {natijalar[0][9]}
        Foydalanuvchi 👤 pul : {natijalar[0][10]}
        """)
        return "TANLA"

    elif text == "💫 Allohning 99ta ismlari ✨":
        ismlari = """
        1️⃣ 🤲 Ar-Rahman – Eng mehribon
2️⃣ 💗 Ar-Rahim – Eng rahmli
3️⃣ 👑 Al-Malik – Butun borliqning podshohi
4️⃣ 🛡️ Al-Quddus – Mukammal pok
5️⃣ ☝️ As-Salam – Tinçlik beruvchi
6️⃣ 🧠 Al-Mu’min – Xavfsizlik va e’tiqod ato etuvchi
7️⃣ 🛡️ Al-Muhaymin – Nigohda tutuvchi, kuzatuvchi
8️⃣ 💪 Al-Aziz – G‘olib va qudratli
9️⃣ 🧭 Al-Jabbar – Irodasini majburan o‘tkazuvchi
🔟 🏗️ Al-Mutakabbir – Buyuklikda yagonadir

11️⃣ 🌍 Al-Khaliq – Yaratgan
12️⃣ 🧬 Al-Bari’ – Sozsiz yaratuvchi
13️⃣ 🎨 Al-Musawwir – Sifat va shakl beruvchi
14️⃣ 🎁 Al-Ghaffar – Gunohlarni ko‘p mag‘firat qiluvchi
15️⃣ 🌦️ Al-Qahhar – Mutlaq g‘alaba qiluvchi
16️⃣ 🎓 Al-Wahhab – Behisob in’om qiluvchi
17️⃣ 🛍️ Ar-Razzaq – Rizq beruvchi
18️⃣ ⚖️ Al-Fattah – Yechim beruvchi, ochuvchi
19️⃣ 🧠 Al-‘Alim – Biluvchi
2️⃣0️⃣ 🕰️ Al-Qabid – Qisqartiruvchi, toraytiruvchi

21️⃣ 💨 Al-Basit – Kengaytiruvchi, yoyuvchi
22️⃣ 🛑 Al-Khafid – Pastlatuvchi
23️⃣ 🧗‍♂️ Ar-Rafi’ – Ko‘taruvchi
24️⃣ 🥇 Al-Mu’izz – Ulug‘lovchi
25️⃣ 🕳️ Al-Mudhill – Xorlovchi
26️⃣ ⚖️ As-Sami’ – Eshituvchi
27️⃣ 👁️ Al-Basir – Ko‘ruvchi
28️⃣ 📏 Al-Hakam – Hukm qiluvchi
29️⃣ 🧩 Al-‘Adl – Adolatli
3️⃣0️⃣ 🛑 Al-Latif – Yaxshi niyat bilan nozik ish qiluvchi

31️⃣ 🕊️ Al-Khabir – Hamma narsadan xabardor
32️⃣ 🎀 Al-Halim – Yumshoq, sabrli
33️⃣ 🎉 Al-‘Azim – Buyuk
34️⃣ 🧱 Al-Ghaffur – Kechiruvchi
35️⃣ 🕋 Ash-Shakur – Qadrdonlik qiluvchi
36️⃣ 🕰️ Al-‘Aliyy – Yuksak
37️⃣ 🧠 Al-Kabir – Katta
38️⃣ 🧠 Al-Hafiz – Himoya qiluvchi
39️⃣ 🧘‍♂️ Al-Muqit – Quvvat beruvchi
4️⃣0️⃣ 📜 Al-Hasib – Hisoblovchi

41️⃣ 💎 Al-Jalil – Ulug‘vor
42️⃣ 🕊️ Al-Karim – Saxiy
43️⃣ 💡 Ar-Raqib – Nazorat qiluvchi
44️⃣ 📖 Al-Mujib – Duolarga javob beruvchi
45️⃣ 🧱 Al-Wasi’ – Cheksiz
46️⃣ 🎯 Al-Hakim – Dono
47️⃣ 🛡️ Al-Wadud – Muhabbatli
48️⃣ 💬 Al-Majid – Ulug‘
49️⃣ 🏗️ Al-Ba’ith – Qayta tiriltiruvchi
5️⃣0️⃣ ⏳ Ash-Shahid – Guvoh bo‘luvchi

51️⃣ 🧠 Al-Haqq – Haqiqat egasi
52️⃣ 🧭 Al-Wakil – Ishonchli vakil
53️⃣ 🚪 Al-Qawiyy – Qudratli
54️⃣ 🛡️ Al-Matin – Mustahkam
55️⃣ 👑 Al-Waliyy – Do‘st va hokim
56️⃣ 🧬 Al-Hamid – Maqtovga loyiq
57️⃣ 🔁 Al-Muhsi – Sanovchi
58️⃣ 🧠 Al-Mubdi’ – Birinchi yaratuvchi
59️⃣ 🔄 Al-Mu’id – Qaytaruvchi
6️⃣0️⃣ 🔥 Al-Muhyi – Hayot beruvchi

61️⃣ 🧊 Al-Mumit – O‘ldiruvchi
62️⃣ 🧠 Al-Hayy – Tiriklik egasi
63️⃣ 🕰️ Al-Qayyum – O‘z-o‘zidan mavjud
64️⃣ 📿 Al-Wajid – Topuvchi
65️⃣ 💰 Al-Majid – Sharafli
66️⃣ 🧠 Al-Wahid – Yagona
67️⃣ 💫 As-Samad – Hamma narsa unga muhtoj
68️⃣ 🧠 Al-Qadir – Qodir
69️⃣ 💫 Al-Muqtadir – Quvvatli ijro etuvchi
7️⃣0️⃣ 🧭 Al-Muqaddim – Oldinga suruvchi

71️⃣ 🛑 Al-Mu’akhkhir – Orqaga suruvchi
72️⃣ 👁️‍🗨️ Al-Awwal – Birinchi
73️⃣ 🔚 Al-Akhir – Oxirgi
74️⃣ 🧱 Az-Zahir – Ayan
75️⃣ 🕳️ Al-Batin – Yashirin
76️⃣ 💡 Al-Wali – Hamma narsani boshqaruvchi
77️⃣ 👁️ Al-Muta’ali – Oliylik egasi
78️⃣ ⚖️ Al-Barr – Ezgulik qiluvchi
79️⃣ 📜 At-Tawwab – Tavbalarni qabul qiluvchi
8️⃣0️⃣ 🧠 Al-Muntaqim – Jazolovchi

81️⃣ 🧘‍♂️ Al-‘Afuww – Afv etuvchi
82️⃣ 🧠 Ar-Ra’uf – Mehribon
83️⃣ 📦 Malik-ul-Mulk – Mulklarning podshohi
84️⃣ 🧭 Dhul-Jalali wal-Ikram – Ulug‘lik va karam egasi
85️⃣ 🔁 Al-Muqsit – Adolat bilan bo‘luvchi
86️⃣ 🔐 Al-Jami’ – Jamlovchi
87️⃣ ⏰ Al-Ghaniyy – Behojat
88️⃣ 🛐 Al-Mughni – Boy qiluvchi
89️⃣ 🔁 Al-Mani’ – To‘xtatuvchi
9️⃣0️⃣ 🌩️ Ad-Darr – Zarar yetkazuvchi

91️⃣ 💧 An-Nafi’ – Foyda beruvchi
92️⃣ ⏳ An-Nur – Nur sochuvchi
93️⃣ 🌏 Al-Hadi – Yo‘l ko‘rsatuvchi
94️⃣ 🔁 Al-Badi’ – Betakror yaratuvchi
95️⃣ 📊 Al-Baqi – Doimiy
96️⃣ ⚖️ Al-Warith – Mulk vorisi
97️⃣ 🧠 Ar-Rashid – To‘g‘ri yo‘l ko‘rsatuvchi
98️⃣ 🤲 As-Sabur – Sabrli
99️⃣ 🕌 Allah – Hammasining egasi
        """
        update.message.reply_text(text=ismlari)
        return "TANLA"
    elif text == "Kartaga pul qo'shish 💳":
        update.message.reply_text(text="Foydalanuvchi 👤 ismi ")
        return "KARTAGA_PUL_QOSHISH_ISM"
    elif text == "Profil uchun rasmlar 👑":
        global rasm_raqam
        rasm_raqam = 1
        buttons = [[InlineKeyboardButton("➡️", callback_data="➡️")]]
        markup = InlineKeyboardMarkup(buttons)

        with open(f"fon{rasm_raqam}.jpg", "rb") as photo:
            context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=photo,
                caption="Profil uchun rasmlar 👑",
                reply_markup=markup
            )
        return "TANLA"

    elif text == "Kartadan pul yechish 💰":
        update.message.reply_text(text="Foydalanuvchi 👤 ismi ")
        return "KARTAGA_PUL_YECHISH_ISM"


    elif text == "bexruzni rasmi":
        update.message.reply_text(text="https://t.me/pul_hisoblari/464")
        return "TANLA"



    elif text == "diyorjonni rasmi":
        update.message.reply_text(text="https://t.me/pul_hisoblari/465")
        return "TANLA"




    elif text == context.user_data['true']:
        global captchani_soni
        captchani_soni += 1
        update.message.reply_text(text="🎉")
        update.message.reply_text(text="Botdan foydalanishingiz mumkin 😊 🎉🎉🎉")
        start(update, context)
        return "TANLA"



    elif text == context.user_data['x1']:
        update.message.reply_text(text="❌")
        update.message.reply_text(text="Xato boshqattan urining 🧮")
        xato_captcha(update, context)
        return "TANLA"


    elif text == context.user_data['x2']:
        update.message.reply_text(text="❌")
        update.message.reply_text(text="Xato boshqattan urining 🧮")
        xato_captcha(update, context)
        return "TANLA"


    elif text == context.user_data['x3']:
        update.message.reply_text(text="❌")
        update.message.reply_text(text="Xato boshqattan urining 🧮")
        xato_captcha(update, context)
        return "TANLA"



    elif text == "Ruscha qo'shiqlar 🎶":
        update.message.reply_text("https://t.me/pul_hisoblari/257")
        update.message.reply_text("https://t.me/pul_hisoblari/268")
        update.message.reply_text("https://t.me/pul_hisoblari/269")
        update.message.reply_text("https://t.me/pul_hisoblari/270")
        update.message.reply_text("https://t.me/pul_hisoblari/271")
        update.message.reply_text("https://t.me/pul_hisoblari/272")
        update.message.reply_text("https://t.me/pul_hisoblari/273")
        update.message.reply_text("https://t.me/pul_hisoblari/274")
        update.message.reply_text("https://t.me/pul_hisoblari/275")
        update.message.reply_text("https://t.me/pul_hisoblari/276")
        update.message.reply_text("https://t.me/pul_hisoblari/411")
        update.message.reply_text("https://t.me/pul_hisoblari/415")
        update.message.reply_text("https://t.me/pul_hisoblari/416")
        update.message.reply_text("https://t.me/pul_hisoblari/422")
        update.message.reply_text("https://t.me/pul_hisoblari/423")
        update.message.reply_text("https://t.me/pul_hisoblari/424")
        update.message.reply_text("https://t.me/pul_hisoblari/426")
        update.message.reply_text("https://t.me/pul_hisoblari/427")
        update.message.reply_text("https://t.me/pul_hisoblari/429")
        update.message.reply_text("https://t.me/pul_hisoblari/434")
        update.message.reply_text("https://t.me/pul_hisoblari/435")
        update.message.reply_text("https://t.me/pul_hisoblari/437")
        update.message.reply_text("https://t.me/pul_hisoblari/483")
        update.message.reply_text("https://t.me/pul_hisoblari/484")
        update.message.reply_text("https://t.me/pul_hisoblari/485")
        update.message.reply_text("https://t.me/pul_hisoblari/486")
        return "TANLA"

    elif text == "📖 Kitoblar ✨":
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/606")
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/161")
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/151")
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/3141")
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/2883")
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/107")
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/111")
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/113")
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/116")
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/119")
        update.message.reply_text("https://t.me/pdf_audio_kitoblar_elektron/83")
        update.message.reply_text("📖❤️✅")

    elif text == "Inglishcha qo'shiqlar 🎶":
        update.message.reply_text("https://t.me/pul_hisoblari/277")
        update.message.reply_text("https://t.me/pul_hisoblari/278")
        update.message.reply_text("https://t.me/pul_hisoblari/279")
        update.message.reply_text("https://t.me/pul_hisoblari/280")
        update.message.reply_text("https://t.me/pul_hisoblari/281")
        update.message.reply_text("https://t.me/pul_hisoblari/282")
        update.message.reply_text("https://t.me/pul_hisoblari/283")
        update.message.reply_text("https://t.me/pul_hisoblari/284")
        update.message.reply_text("https://t.me/pul_hisoblari/285")
        update.message.reply_text("https://t.me/pul_hisoblari/286")
        update.message.reply_text("https://t.me/pul_hisoblari/412")
        update.message.reply_text("https://t.me/pul_hisoblari/417")
        update.message.reply_text("https://t.me/pul_hisoblari/418")
        update.message.reply_text("https://t.me/pul_hisoblari/419")
        update.message.reply_text("https://t.me/pul_hisoblari/420")
        update.message.reply_text("https://t.me/pul_hisoblari/421")
        update.message.reply_text("https://t.me/pul_hisoblari/430")
        update.message.reply_text("https://t.me/pul_hisoblari/436")

        return "TANLA"
    elif text == "Turk qo'shiqlar 🎶":

        update.message.reply_text("https://t.me/pul_hisoblari/287")
        update.message.reply_text("https://t.me/pul_hisoblari/288")
        update.message.reply_text("https://t.me/pul_hisoblari/289")
        update.message.reply_text("https://t.me/pul_hisoblari/290")
        update.message.reply_text("https://t.me/pul_hisoblari/291")
        update.message.reply_text("https://t.me/pul_hisoblari/292")
        update.message.reply_text("https://t.me/pul_hisoblari/293")
        update.message.reply_text("https://t.me/pul_hisoblari/294")
        update.message.reply_text("https://t.me/pul_hisoblari/295")
        update.message.reply_text("https://t.me/pul_hisoblari/296")
        update.message.reply_text("https://t.me/pul_hisoblari/413")
        update.message.reply_text("https://t.me/pul_hisoblari/414")
        update.message.reply_text("https://t.me/pul_hisoblari/425")
        update.message.reply_text("https://t.me/pul_hisoblari/431")
        update.message.reply_text("https://t.me/pul_hisoblari/433")

        return "TANLA"
    elif text == "🎧 My music 🖤":
        k = [
            [KeyboardButton(text="Ruscha qo'shiqlar 🎶")],
            [KeyboardButton(text="Inglishcha qo'shiqlar 🎶")],
            [KeyboardButton(text="Turk qo'shiqlar 🎶")],
            [KeyboardButton(text="💫 Menyuga qaytish ⬅️")],
        ]
        update.message.reply_text(text="Qo'shiq turi 🎵", reply_markup=ReplyKeyboardMarkup(k, resize_keyboard=True))
        return "TANLA"


    elif text == "Kartadan kartaga pul o'tgazish  💳  🔜  🪪":
        update.message.reply_text(text="Pul beruvchi odam ismi ➖💳 ")
        return "PUL_BERUVCHI"
    elif text == "Nussa va Rarra tanishamiz":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13365")
        return "TANLA"
    elif text == "🚲 Bismillahni fazilati":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13371")
        return "TANLA"
    elif text == "😊 Tabassum sadaqadir":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13372")
        return "TANLA"
    elif text == "OYIMGA OXSHASHNI ISTAYMAN":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13378")
        return "TANLA"
    elif text == "MAHRAM EMAS":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13380")
        return "TANLA"
    elif text == "QOLGAN ISHGA QOR YOG'AR":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13381")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (1-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/31")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (2-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/32")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (3-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/33")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (4-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/34")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (5-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/35")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (6-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/36")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (7-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/4885")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (8-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/4886")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (9-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/10775")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (10-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/10776")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (11-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13132")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (12-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13133")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (13-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13142")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (14-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13143")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (15-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13148")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (16-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13149")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (17-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13159")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (18-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13160")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (19-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13169")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (20-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13170")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (21-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13181")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (22-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13182")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (23-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13191")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (24-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13192")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (25-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13201")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (26-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13202")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (27-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13211")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (28-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13212")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (29-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13221")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (30-qism, 1-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13222")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (1-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13231")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (2-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13232")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (3-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13240")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (4-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13241")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (5-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13250")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (6-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13251")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (7-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13262")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (8-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13263")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (9-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13273")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (10-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13274")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (11-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13283")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (12-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13284")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (13-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13298")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (14-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13299")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (15-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13307")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (16-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13308")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (17-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13315")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (18-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13316")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (19-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13325")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (20-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13326")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (21-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13335")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (22-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13336")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (23-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13346")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (24-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13347")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (25-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13354")
        return "TANLA"
    elif text == "📹 Allohning Habibi Muhammad (26-qism, 2-fasl)":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13355")
        return "TANLA"
    elif text == "ONA MEHRI":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13436")
        return "TANLA"
    elif text == "BIRGALASHIB ZIKR QILAYLIK":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13435")
        return "TANLA"
    elif text == "SIZ OLARMIDINGIZ?":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13428")
        return "TANLA"
    elif text == "TAJRIBA":
        update.message.reply_text(text="https://t.me/lsIomiy_Multfilm/13429")
        return "TANLA"


    elif text == "👑 Islomiy multfilimlar 🎞":
        k = [
            [KeyboardButton(text="Nussa va Rarra tanishamiz"), KeyboardButton(text="🚲 Bismillahni fazilati")],
            [KeyboardButton(text="😊 Tabassum sadaqadir"), KeyboardButton(text="OYIMGA OXSHASHNI ISTAYMAN")],
            [KeyboardButton(text="MAHRAM EMAS"), KeyboardButton(text="QOLGAN ISHGA QOR YOG'AR")],
            [KeyboardButton(text="ONA MEHRI"), KeyboardButton(text="BIRGALASHIB ZIKR QILAYLIK")],
            [KeyboardButton(text="SIZ OLARMIDINGIZ?"), KeyboardButton(text="TAJRIBA")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (1-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (2-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (3-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (4-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (5-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (6-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (7-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (8-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (9-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (10-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (11-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (12-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (13-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (14-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (15-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (16-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (17-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (18-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (19-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (20-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (21-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (22-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (23-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (24-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (25-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (26-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (27-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (28-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (29-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (30-qism, 1-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (1-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (2-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (3-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (4-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (5-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (6-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (7-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (8-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (9-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (10-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (11-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (12-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (13-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (14-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (15-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (16-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (17-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (18-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (19-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (20-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (21-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (22-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (23-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (24-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (25-qism, 2-fasl)")],
            [KeyboardButton(text="📹 Allohning Habibi Muhammad (26-qism, 2-fasl)")],
            [KeyboardButton(text="💫 Menyuga qaytish ⬅️")],
        ]
        update.message.reply_text(text="Tanlang", reply_markup=ReplyKeyboardMarkup(k, resize_keyboard=True))
        return "TANLA"

    elif text == "Kartadagi pulni ko'rish 💰":
        update.message.reply_text(text="Foydalanuvchi 👤 ismi ")
        return "PUL_KORISH_ISM"
    elif text == "Savol berish 🪐":
        update.message.reply_text("Savol bering faqat aniq bayon qiling. 🧾 ")
        return "SAVOL_BER"
    elif text == "Ro'yxatdan o'tganlarni ko'rish 📋":
        con = sqlite3.connect("hisoblar.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users;")
        natija = cur.fetchall()
        for i in natija:
            update.message.reply_text(text=f"""
Foydalanuvchi ismi 👤 🔜 {i[5]}
Foydalanuvchi familyasi 📰 🔜 {i[6]}
Foydalanuvchi yoshi 📆 🔜 {i[7]}
Foydalanuvchi plui 💰 🔜 {i[10]}
Foydalanuvchi ro'yxatdan o'tgan vaqti ⏳ 🔜 {i[4]}
            """)
        cur.close()
        con.close()
        return "TANLA"
    elif text == "Boshiga qaytish👑 ⬅️":
        K = [
            [KeyboardButton("💫 Bosh sahifaga maytaman 👌🏻"), KeyboardButton("💫 Bosh sahifaga maytmayman ❌")],
            [KeyboardButton("💫 Menyuga qaytish ⬅️")]
        ]
        update.message.reply_text(text="Qaymoqchi bo'lsangiz  '💫 Bosh sahifaga maytaman 👌🏻'  tugmasini boshing. ",
                                  reply_markup=ReplyKeyboardMarkup(K, resize_keyboard=True))
        return "TANLA"
    elif text == "💫 Menyuga qaytish ⬅️":

        update.message.reply_text("☘️ Asosiy menyu ✨", parse_mode="Markdown",
                                  reply_markup=ReplyKeyboardMarkup(bosh_menyu, one_time_keyboard=False,
                                                                   resize_keyboard=True))
        return "TANLA"
    elif text == "Foydalanuvchi ismini o'zgartirish 👤":
        update.message.reply_text(text="Foydalanuvchi 👤 ismi ")
        return "Foydalanuvchi_ismini_ozgartirish_ISMI"
    elif text == "Foydalanuvchi parolini o'zgartirish 🔒":
        update.message.reply_text(text="Foydalanuvchi 👤 ismi ")
        return "Foydalanuvchi_parolini_ozgartirish_ISMI"
    elif text == "Yon daftardagi qaydni ko'rish 📨":
        con = sqlite3.connect('hisoblar.db')
        cur = con.cursor()
        cur.execute("SELECT qayd_nomi,qayd FROM qaydlar WHERE ism=?;", (context.user_data["Yon_daftar_ism"],))
        n = cur.fetchall()
        if not n:
            update.message.reply_text("Qaydlar yo'q 📭")
        for i in n:
            qayd_nomi = f"{i[0]}"
            qayd = f"{i[1]}"
            update.message.reply_text(text=f"Qayd nomi ➡️ *{qayd_nomi}*\t\t\n\nQayt ⬇️\n\n{qayd}",
                                      parse_mode="Markdown")
        con.commit()
        cur.close()
        return "TANLA"

    elif text == "⚙️ Sozlamalar":
        K = [
            [KeyboardButton("Foydalanuvchi ismini o'zgartirish 👤"),
             KeyboardButton("Foydalanuvchi parolini o'zgartirish 🔒")],
            [KeyboardButton("💫 Menyuga qaytish ⬅️")]
        ]
        update.message.reply_text(text="Foydalanuvchi sozlamalari 👤",
                                  reply_markup=ReplyKeyboardMarkup(K, resize_keyboard=True))
        return "TANLA"
    elif text == "💫 Bosh sahifaga maytaman 👌🏻":
        update.message.reply_text("*Bosh sahifaga qaytish uchun menga birorta narsa buboring*", parse_mode="Markdown")
        return "START"
    elif text == "Yon daftarga qayd yozish 📝":
        update.message.reply_text(
            "*Qayd* nomini kiriting ✏️\n\n _Qayd nomi bu sarlavxasi desayam bo'ladi_\n\n📌 _Eslatma siz kiritgan qayd nomi so'zida orasida bo'sh joy o'rniga avtomitik ravishda pastgi chiziq qo'yiladi ❗️_",
            parse_mode="Markdown")
        return "qayd_nomi"
    elif text == "SMS ✉️ yuborish":
        update.message.reply_text("*Kimga qaysi foydalanuvchiga 🤷🏼‍♂️\nFoydalanuvchi ismi 👤*", parse_mode="Markdown")
        return "sms_ism"

    elif text == "Yon daftardagi qaydni o'chirish 🗑":
        update.message.reply_text("O'chirmoqchi bo'lgan *qayd* nomini kiriting ✏️", parse_mode="Markdown")
        return "ochirmoqchi_bolgan_qayd_nomi"

    elif text == "Yon daftardagi hamma qaydni o'chirish 🗑":
        con = sqlite3.connect("hisoblar.db")
        cur = con.cursor()
        cur.execute("DELETE FROM qaydlar WHERE ism=?", (context.user_data["Yon_daftar_ism"],))
        con.commit()
        cur.close()
        update.message.reply_text("Hamma qaydni o'chirildi 🗑 ✅")
        return "TANLA"

    elif text == "Yon daftardagi qaydni almashtirish ✂️":
        K = [
            [KeyboardButton("Qayd nomini o'zgartirish 🔁"),
             KeyboardButton("Qaydni o'zgartirish 🔁")],
            [KeyboardButton("✨ Menyuga qaytish ⬅️")]
        ]
        update.message.reply_text(text="Qaydlarni sozlash 🛠",
                                  reply_markup=ReplyKeyboardMarkup(K, resize_keyboard=True))
        return "TANLA"

    elif text == "Qayd nomini o'zgartirish 🔁":
        update.message.reply_text("O'zgartirmoqchi bo'lgan *qayd* nomini kiriting ✏️", parse_mode="Markdown")
        return "ozgartirmoqchi_bolgan_qayd_nomi"

    elif text == "Qaydni o'zgartirish 🔁":
        update.message.reply_text("O'zgartirmoqchi bo'lgan *qayd* nomini kiriting ✏️", parse_mode="Markdown")
        return "ozgartirmoqchi_bolgan_qayd"

    elif text == "😜 Adminga savol berish ✨":
        update.message.reply_text(f"Salom {update.message.from_user.first_name} menga savol berishingiz mumkin 😊",
                                  parse_mode="Markdown")
        return "adminga_savol_berish"

    elif text == "✨ Menyuga qaytish ⬅️":
        k = [
            [KeyboardButton(text="Yon daftarga qayd yozish 📝"), KeyboardButton(text="Yon daftardagi qaydni ko'rish 📨")],
            [KeyboardButton(text="Yon daftardagi qaydni o'chirish 🗑"),
             KeyboardButton(text="Yon daftardagi hamma qaydni o'chirish 🗑")],
            [KeyboardButton(text="Yon daftardagi qaydni almashtirish ✂️"), KeyboardButton(text="💫 Menyuga qaytish ⬅️")],
        ]
        update.message.reply_text(text="Qaysi biri 🧐", reply_markup=ReplyKeyboardMarkup(k, resize_keyboard=True))
        update.message.reply_text(text="🧐")
        return "TANLA"

    elif text == "Admin bilan bog'lanish ☘️":

        with open("ahadjon.jpg", "rb") as photo:

            context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=photo,
                caption="""
                 👋 Assalomu alaykum! Men sizga yordam bera olishim uchun adminim bilan bevosita bog‘lanishingiz mumkin.

🔑 Admin: 𝒜𝒽𝒶𝒹𝒿𝑜𝓃🫠❤️– ✅ Tezkor yordam va kerakli qo‘llab-quvvatlash uchun har doim tayyor!

💬 Fikr-mulohazalar yoki savollar bo‘lsa, @Ahadjon_tem1rbekov
                 """
            )
    else:
        update.message.reply_text(
            f"➡️ {text} ⬅️ Bu so'zizga  tushunmadim\n\n🪐 Menyudan foydalanishingiz mumkin /menyu  🌿\n\n⭕️ Yoki pastda xabar yuboradigan joyda 4 ta nuqtani 🎛 bosing menyu ochiladi ❗️")


@captcha
@block
def sms_ism(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute(f"SELECT ism FROM users WHERE ism='{text}';")
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['sms_ism'] = text
                update.message.reply_text(text="Foydalanuvchi 👤 topildi  raxmat ✅")
                update.message.reply_text(text="Xabarni kiriting 📜")
                return "sms_xabar"
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")
        return 'sms_ism'


@captcha
@block
def sms_xabar(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()

    text = update.message.text

    cur.execute("SELECT id FROM users WHERE ism = ?;", (context.user_data['sms_ism'],))
    n = cur.fetchone()

    user_id = n[0]

    # Foydalanuvchining start bosganini log qilish
    id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    user_name = update.message.from_user.username
    vaqt = datetime.now()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sms (
            id INTEGER,
            first_name TEXT,
            last_name TEXT,
            user_name TEXT,
            vaqt TEXT,
            kimga TEXT,
            nima_dep TEXT
        );
    """)
    cur.execute(
        "INSERT INTO sms (id, first_name, last_name, user_name, vaqt,kimga,nima_dep) VALUES (?,?,?, ?, ?, ?, ?)",
        (id, first_name, last_name, user_name, vaqt, context.user_data['sms_ism'], text)
    )
    cur.execute("SELECT ism FROM users WHERE id=?;", (id,))
    toliqism = cur.fetchone()

    toliq = toliqism[0]
    context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=f"""
        🆔 ID: {id}
        👤 Ismi: {first_name}
        👥 Familiyasi: {last_name}
        💬 Username: @{user_name}
        ⏰ Vaqt: {vaqt}

        SMS yubordi ✉️
        """
    )
    con.commit()
    con.close()
    bot = context.bot
    bot.send_message(chat_id=user_id, text=f"""
        🆔 ID: {id}
        👤 Ismi: {first_name}
        👤 To'liq ismi: {toliq}
        👥 Familiyasi: {last_name}
        💬 Username: @{user_name}
        ⏰ Vaqt: {vaqt}

        Sizga xabar yubordi

        Yuborilgan xabar 👇🏻

        {text}
        """)
    update.message.reply_text("Xabar muvaffaqiyatli yuborildi.✅")
    return 'TANLA'


@captcha
@block
def ozgartirmoqchi_bolgan_qayd(update, context):
    text = update.message.text
    con = sqlite3.connect("hisoblar.db")
    cur = con.cursor()
    cur.execute("SELECT qayd_nomi FROM qaydlar WHERE ism=?;",
                (context.user_data["Yon_daftar_ism"],))  # bazadagi ismlar ham kichik holatda olinadi
    natijalar = cur.fetchall()
    topildi = False
    for row in natijalar:
        if row[0] == text:
            topildi = True
            break
    if topildi:
        context.user_data['ozgartirmoqchi_bolgan_qayd'] = text
        update.message.reply_text("Raxmat qayd nomi topildi ✅")
        update.message.reply_text(
            " Yangi *qaydni*  kiriting ✏️",
            parse_mode="Markdown")
        return "new_qayd"
    else:
        update.message.reply_text("Uzur, bunday qayd nomi mavjud emas. ✅\n\nBoshqa qayd nomi kiriting 😉")
        update.message.reply_text("Qaydni kiriting 📝")
        return "ozgartirmoqchi_bolgan_qayd"


@captcha
@block
def adminga_savol_berish(update, context):
    text = update.message.text
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    print(first_name)
    last_name = update.message.from_user.last_name
    user_name = update.message.from_user.username
    vaqt = datetime.now()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS adminga_Savol (
        id INTEGER,
        first_name TEXT,
        last_name TEXT,
        user_name TEXT,
        vaqt TEXT,
        adminga_Savol TEXT
    );
    """)

    cur.execute(
        "INSERT INTO adminga_Savol (id, first_name, last_name, user_name, vaqt,adminga_Savol) VALUES (?,?, ?, ?, ?, ?)",
        (id, first_name, last_name, user_name, vaqt, text)
    )
    con.commit()

    update.message.reply_text("✨ Raxmat savol saqlandi 📩 sizga 2-3 soatlarda murojatga chiqadi\n\n👑")
    return 'TANLA'


@captcha
@block
def ozgartirmoqchi_bolgan_qayd_nomi(update, context):
    text = update.message.text
    con = sqlite3.connect("hisoblar.db")
    cur = con.cursor()
    cur.execute("SELECT qayd_nomi FROM qaydlar WHERE ism=?;",
                (context.user_data["Yon_daftar_ism"],))  # bazadagi ismlar ham kichik holatda olinadi
    natijalar = cur.fetchall()
    topildi = False
    for row in natijalar:
        if row[0] == text:
            topildi = True
            break
    if topildi:
        context.user_data['ozgartirmoqchi_bolgan_qayd_nomi'] = text
        update.message.reply_text("Raxmat qayd nomi topildi ✅")
        update.message.reply_text(
            " Yangi *qayd* nomini kiriting ✏️\n\n _Qayd nomi bu sarlavxasi desayam bo'ladi_\n\n📌 _Eslatma siz kiritgan qayd nomi so'zida orasida bo'sh joy o'rniga avtomitik ravishda pastgi chiziq qo'yiladi ❗️_",
            parse_mode="Markdown")
        return "new_qayd_lik"
    else:
        update.message.reply_text("Uzur, bunday qayd nomi mavjud emas. ✅\n\nBoshqa qayd nomi kiriting 😉")
        update.message.reply_text("Qaydni kiriting 📝")
        return "ozgartirmoqchi_bolgan_qayd_nomi"


@captcha
@block
def new_qayd_lik(update, context):
    ism = update.message.text
    con = sqlite3.connect("hisoblar.db")
    cur = con.cursor()
    cur.execute("SELECT qayd_nomi FROM qaydlar")  # bazadagi ismlar ham kichik holatda olinadi
    natijalar = cur.fetchall()
    topildi = False
    for row in natijalar:
        if row[0] == ism:
            topildi = True
            break
    if topildi:
        update.message.reply_text("Uzur, bunday qayd nomi mavjud. ✅\n\nBoshqa qayd nomi kiriting 😉")
        update.message.reply_text("Yangi *qayd* nomini kiriting ✏️", parse_mode="Markdown")
        return "new_qayd_lik"
    else:
        text = update.message.text
        context.user_data['new_qayd_lik'] = text
        con = sqlite3.connect("hisoblar.db")
        cur = con.cursor()
        cur.execute("UPDATE qaydlar SET qayd_nomi=? WHERE qayd_nomi=?;",
                    (context.user_data["new_qayd_lik"], context.user_data["ozgartirmoqchi_bolgan_qayd_nomi"]))
        con.commit()
        cur.close()
        update.message.reply_text("Qayd nomi o'zgartirildi ✅")
        return "TANLA"


@captcha
@block
def new_qayd(update, context):
    text = update.message.text
    context.user_data['new_qayd'] = text
    con = sqlite3.connect("hisoblar.db")
    cur = con.cursor()
    cur.execute("UPDATE qaydlar SET qayd=? WHERE qayd_nomi=?;",
                (context.user_data["new_qayd"], context.user_data["ozgartirmoqchi_bolgan_qayd"]))
    con.commit()
    cur.close()
    update.message.reply_text("Qayd o'zgartirildi ✅")
    return "TANLA"


@captcha
@block
def ochirmoqchi_bolgan_qayd_nomi(update, context):
    text = update.message.text
    con = sqlite3.connect("hisoblar.db")
    cur = con.cursor()
    cur.execute("SELECT qayd_nomi FROM qaydlar WHERE ism=?;",
                (context.user_data["Yon_daftar_ism"],))  # bazadagi ismlar ham kichik holatda olinadi
    natijalar = cur.fetchall()
    topildi = False
    for row in natijalar:
        if row[0] == text:
            topildi = True
            break
    if topildi:
        context.user_data['ochirmoqchi_bolgan_qayd_nomi'] = text
        cur.execute("DELETE FROM qaydlar WHERE qayd_nomi=?", (context.user_data["ochirmoqchi_bolgan_qayd_nomi"],))
        con.commit()
        update.message.reply_text("Qaydni o'chirildi 🗑 ✅")
        return "TANLA"
    else:
        update.message.reply_text("Uzur, bunday qayd nomi mavjud emas. ✅\n\nBoshqa qayd nomi kiriting 😉")
        update.message.reply_text("Qaydni kiriting 📝")
        return "ochirmoqchi_bolgan_qayd_nomi"


@captcha
@block
def yon_daftardagi_qaydni_korish_parol(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT parol FROM users WHERE ism=? ;", (context.user_data['yon_daftardagi_qaydni_korish_ism'],))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['yon_daftardagi_qaydni_korish_parol'] = text
                update.message.reply_text(text="To'ri raxmat ✅")
                return "TANLA"
            else:
                update.message.reply_text(text="Parol xato ❌ ")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def qayd_nomi(update, context):
    ism = update.message.text
    con = sqlite3.connect("hisoblar.db")
    cur = con.cursor()
    cur.execute("SELECT qayd_nomi FROM qaydlar;")  # bazadagi ismlar ham kichik holatda olinadi
    natijalar = cur.fetchall()
    topildi = False
    for row in natijalar:
        if row[0] == ism:
            topildi = True
            break
    if topildi:
        update.message.reply_text("Uzur, bunday qayd nomi mavjud. ✅\n\nBoshqa qayd nomi kiriting 😉")
        update.message.reply_text("Qaydni kiriting 📝")
        return "qayd_nomi"
    else:
        text = ism.replace(" ", "_")
        context.user_data['qayd_nomi'] = text
        update.message.reply_text(text="Raxmat ✅")
        update.message.reply_text(text="Qaydni kiriting 📝")
        return "qayd"


@captcha
@block
def qayd(update, context):
    text = update.message.text
    context.user_data['qayd'] = text
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    print(first_name)
    last_name = update.message.from_user.last_name
    user_name = update.message.from_user.username
    vaqt = datetime.now()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS qaydlar (
        id INTEGER,
        first_name TEXT,
        last_name TEXT,
        user_name TEXT,
        vaqt TEXT,
        qayd_nomi TEXT,
        qayd TEXT,
        ism TEXT,
        parol TEXT
    );
    """)
    cur.execute(
        "INSERT INTO qaydlar (id, first_name, last_name, user_name, vaqt,qayd_nomi,qayd,ism,parol) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)",
        (id, first_name, last_name, user_name, vaqt, context.user_data['qayd_nomi'], context.user_data['qayd'],
         context.user_data['Yon_daftar_ism'], context.user_data['Yon_daftar_parol'])
    )
    con.commit()
    update.message.reply_text(text="Raxmat ✅")
    update.message.reply_text(text="Qayd saqlandi 📥")
    return "TANLA"


@captcha
@block
def Foydalanuvchi_ismini_ozgartirish_ISMI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT ism FROM users WHERE ism=? ;", (text,))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['Foydalanuvchi_ismini_ozgartirish_ISMI'] = text
                update.message.reply_text(text="Foydalanuvchi 👤 topildi  raxmat ✅")
                update.message.reply_text(text=f"{text}ni paroli ")
                return "Foydalanuvchi_ismini_ozgartirish_PAROLI"
            else:
                update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def Yon_daftar_ism(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT ism FROM users WHERE ism=? ;", (text,))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['Yon_daftar_ism'] = text
                update.message.reply_text(text="Foydalanuvchi 👤 topildi  raxmat ✅")
                update.message.reply_text(text=f"{text}ni paroli ")
                return "Yon_daftar_parol"
            else:
                update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def Yon_daftar_parol(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT parol FROM users WHERE ism=? ;", (context.user_data['Yon_daftar_ism'],))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['Yon_daftar_parol'] = text
                update.message.reply_text(text="To'ri raxmat ✅")
                k = [
                    [KeyboardButton(text="Yon daftarga qayd yozish 📝"),
                     KeyboardButton(text="Yon daftardagi qaydni ko'rish 📨")],
                    [KeyboardButton(text="Yon daftardagi qaydni o'chirish 🗑"),
                     KeyboardButton(text="Yon daftardagi hamma qaydni o'chirish 🗑")],
                    [KeyboardButton(text="Yon daftardagi qaydni almashtirish ✂️"),
                     KeyboardButton(text="💫 Menyuga qaytish ⬅️")],
                ]
                update.message.reply_text(text="Qaysi biri 🧐",
                                          reply_markup=ReplyKeyboardMarkup(k, resize_keyboard=True))
                update.message.reply_text(text="🧐")
                return "TANLA"
            else:
                update.message.reply_text(text="Parol xato ❌ ")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def Foydalanuvchi_ismini_ozgartirish_PAROLI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT parol FROM users WHERE ism=? ;",
                    (context.user_data['Foydalanuvchi_ismini_ozgartirish_ISMI'],))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['Foydalanuvchi_ismini_ozgartirish_PAROLI'] = text
                update.message.reply_text(text="To'ri raxmat ✅")
                update.message.reply_text(text="Yangi ismni kiriting ✏️")
                return "YANGI_FOYDALANUVCHI_ISMI"
            else:
                update.message.reply_text(text="Parol xato ❌ ")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def YANGI_FOYDALANUVCHI_ISMI(update, context):
    ism = update.message.text
    con = sqlite3.connect("hisoblar.db")
    cur = con.cursor()
    cur.execute("SELECT ism FROM users")  # bazadagi ismlar ham kichik holatda olinadi
    natijalar = cur.fetchall()
    topildi = False
    for row in natijalar:
        if row[0] == ism:
            topildi = True
            break
    if topildi:
        update.message.reply_text("Uzur, bunday foydalanuvchi mavjud. ✅\n\nBoshqa ism kiriting 😉")
        update.message.reply_text("Foydalanuvchi 👤 ismi ")
        return "YANGI_FOYDALANUVCHI_ISMI"
    else:
        cur.execute("UPDATE users SET ism = ? WHERE ism = ?",
                    (ism, context.user_data['Foydalanuvchi_ismini_ozgartirish_ISMI']))
        con.commit()
        cur.close()
        con.close()
        id = update.message.from_user.id
        first_name = update.message.from_user.first_name
        print(first_name)
        last_name = update.message.from_user.last_name
        user_name = update.message.from_user.username
        vaqt = datetime.now()
        context.bot.send_message(
            chat_id=CHANNEL_USERNAME,
            text=f"""
            🆔 ID: {id}
            👤 Ismi: {first_name}
            👥 Familiyasi: {last_name}
            💬 Username: @{user_name}
            ⏰ Vaqt: {vaqt}
            👤 To'liq ism: {ism}
            📝 Ism o'zgaririldi: {ism}

            {context.user_data['Foydalanuvchi_ismini_ozgartirish_ISMI']} ismi {ism} ismiga o'zgaririldi 📝
            👍
            """
        )

        update.message.reply_text("Foydalanuvchi ismi o'zgartirildi ✅")
        return "TANLA"


################################################################
@captcha
@block
def Foydalanuvchi_parolini_ozgartirish_ISMI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT ism FROM users WHERE ism=? ;", (text,))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['Foydalanuvchi_parolini_ozgartirish_ISMI'] = text
                update.message.reply_text(text="Foydalanuvchi 👤 topildi  raxmat ✅")
                update.message.reply_text(text=f"{text}ni paroli ")
                return "Foydalanuvchi_parolini_ozgartirish_PAROLI"
            else:
                update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def Foydalanuvchi_parolini_ozgartirish_PAROLI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT parol FROM users WHERE ism=? ;",
                    (context.user_data['Foydalanuvchi_parolini_ozgartirish_ISMI'],))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['Foydalanuvchi_parolini_ozgartirish_PAROLI'] = text
                update.message.reply_text(text="To'ri raxmat ✅")
                update.message.reply_text(text="Yangi parolni kiriting ✏️")
                return "YANGI_FOYDALANUVCHI_PAROLI"
            else:
                update.message.reply_text(text="Parol xato ❌ ")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def YANGI_FOYDALANUVCHI_PAROLI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    cur.execute("UPDATE users SET parol = ? WHERE ism = ?",
                (text, context.user_data['Foydalanuvchi_parolini_ozgartirish_ISMI']))
    con.commit()
    cur.close()
    con.close()
    id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    print(first_name)
    last_name = update.message.from_user.last_name
    user_name = update.message.from_user.username
    vaqt = datetime.now()
    context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=f"""
        🆔 ID: {id}
        👤 Ismi: {first_name}
        👥 Familiyasi: {last_name}
        💬 Username: @{user_name}
        ⏰ Vaqt: {vaqt}
        👤 To'liq ism: {context.user_data['Foydalanuvchi_parolini_ozgartirish_ISMI']}
        📝 Parol o'zgaririldi: XXXXXXX

        👍
        """
    )
    update.message.reply_text("Foydalanuvchi paroli o'zgartirildi ✅")
    return "TANLA"


################################################################
@captcha
@block
def colbeckdata(update, context):
    global rasm_raqam
    query = update.callback_query
    query.answer()

    if query.data == "⬅️":
        rasm_raqam -= 1
    elif query.data == "➡️":
        rasm_raqam += 1
    if rasm_raqam < 1:
        rasm_raqam = 1
    elif rasm_raqam > 40:
        rasm_raqam = 40
    if rasm_raqam == 1:
        buttons = [[InlineKeyboardButton("➡️", callback_data="➡️")]]
    elif rasm_raqam == 40:
        buttons = [[InlineKeyboardButton("⬅️", callback_data="⬅️")]]

    else:
        buttons = [[InlineKeyboardButton("⬅️", callback_data="⬅️"), InlineKeyboardButton("➡️", callback_data="➡️")]]

    markup = InlineKeyboardMarkup(buttons)

    with open(f"fon{rasm_raqam}.jpg", "rb") as photo:
        context.bot.edit_message_media(
            media=InputMediaPhoto(photo, caption="Profil uchun rasmlar 👑"),
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=markup
        )


@captcha
@block
def SAVOL_BER(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    user_name = update.message.from_user.username
    vaqt = datetime.now()
    savol = update.message.text
    cur.execute("""
    CREATE TABLE IF NOT EXISTS savol_text (
        id INTEGER,
        savol_text TEXT,
        first_name TEXT,
        last_name TEXT,
        user_name TEXT,
        vaqt TEXT
    );
    """)
    cur.execute(
        "INSERT INTO savol_text (id,savol_text, first_name, last_name, user_name, vaqt) VALUES (?,?, ?, ?, ?, ?)",
        (id, savol, first_name, last_name, user_name, vaqt)
    )
    con.commit()
    cur.close()
    con.close()
    k = [
        [InlineKeyboardButton(text="Savolga❗️ javob  ✨ ",
                              url=f"https://chat.openai.com/?q={savol.replace(' ', '+')}"  "")]
    ]
    update.message.reply_text(text="Savolga javob ⬇️", reply_markup=InlineKeyboardMarkup(k))
    return "TANLA"


@captcha
@block
def PUL_KORISH_ISM(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT ism FROM users WHERE ism=? ;", (text,))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['PUL_KORISH_ISM'] = text
                update.message.reply_text(text="Foydalanuvchi 👤 topildi  raxmat ✅")
                update.message.reply_text(text=f"{text}ni paroli ")
                return "PUL_KORISH_PAROLI"
            else:
                update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def PUL_KORISH_PAROLI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT parol FROM users WHERE ism=? ;", (context.user_data['PUL_KORISH_ISM'],))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['PUL_KORISH_PAROLI'] = text
                update.message.reply_text(text="To'ri raxmat ✅")
                cur.execute("SELECT pul FROM users WHERE ism=? ;", (context.user_data['PUL_KORISH_ISM'],))
                n = cur.fetchone()
                for i in n:
                    update.message.reply_text(f" {i} so'm ✅")
                return "TANLA"
            else:
                update.message.reply_text(text="Parol xato ❌ ")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def KARTAGA_PUL_QOSHISH_ISM(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT ism FROM users WHERE ism=? ;", (text,))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['KARTAGA_PUL_QOSHISH_ISM'] = text
                update.message.reply_text(text="Foydalanuvchi 👤 topildi  raxmat ✅")
                update.message.reply_text(text=f"{text}ni paroli ")
                return "KARTAGA_PUL_QOSHISH_PAROLI"
            else:
                update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def KARTAGA_PUL_QOSHISH_PAROLI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT parol FROM users WHERE ism=? ;", (context.user_data['KARTAGA_PUL_QOSHISH_ISM'],))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['KARTAGA_PUL_QOSHISH_PAROLI'] = text
                update.message.reply_text(text="To'gri  raxmat ✅")
                update.message.reply_text(text="Qancha pul qoshilsin")
                return "KARTAGA_PUL_QOSHISH"
            else:
                update.message.reply_text(text="Parol xato  ❌ ")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def PUL_BERUVCHI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT ism FROM users WHERE ism=? ;", (text,))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['PUL_BERUVCHI_ISM'] = text
                update.message.reply_text(text="Foydalanuvchi 👤 topildi  raxmat ✅")
                update.message.reply_text(text=f"{text}ni paroli ")
                return "PUL_BERUVCHI_PAROLI"
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def PUL_BERUVCHI_PAROLI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT parol FROM users WHERE ism=? ;", (context.user_data['PUL_BERUVCHI_ISM'],))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['PUL_BERUVCHI_PAROLI'] = text
                update.message.reply_text(text="To'gri  raxmat ✅")
                update.message.reply_text(text="Pul oluvchi odam ismi ➕💳")
                return "PUL_OLUVCHI"
            else:
                update.message.reply_text(text="Parol xato ❌")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def PUL_OLUVCHI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT ism FROM users WHERE ism=? ;", (text,))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['PUL_OLUVCHI_ISM'] = text
                update.message.reply_text(text="Foydalanuvchi 👤 topildi  raxmat ✅")
                update.message.reply_text(text=f"{text}ni paroli")
                return "PUL_OLUVCHI_PAROLI"
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def PUL_OLUVCHI_PAROLI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT parol FROM users WHERE ism=? ;", (context.user_data['PUL_OLUVCHI_ISM'],))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['PUL_OLUVCHI_PAROLI'] = text
                update.message.reply_text(text="To'gri raxmat ✅")
                update.message.reply_text(text="Qancha pul o'tgazilsin")
                return "QANCHA"
            else:
                update.message.reply_text(text="Parol xato ❌")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def qancha(update, context):
    text = update.message.text
    try:
        context.user_data['qancha_pul_otgazish'] = int(text)
        update.message.reply_text(
            f"Pul miqdori: {text} so'm \nIltimos, davom ettirish uchun 'Tasdiqlash' tugmasini bosing.")
        k = [[KeyboardButton(text="Tasdiqlash ✅")]]
        update.message.reply_text('Pul miqdorini tasdiqlang:',
                                  reply_markup=ReplyKeyboardMarkup(k, one_time_keyboard=True, resize_keyboard=True))
        return "KARTADAN_KARTAGA"
    except ValueError:
        update.message.reply_text("Iltimos, faqat raqam kiriting.")
        return "QANCHA"


@captcha
@block
def KARTADAN_KARTAGA(update, context):
    if 'qancha_pul_otgazish' not in context.user_data:
        update.message.reply_text("Iltimos, avval pul miqdorini kiriting.")
        return "TANLA"

    pul_miqdori = context.user_data['qancha_pul_otgazish']
    try:
        with sqlite3.connect('hisoblar.db') as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET pul = pul - ? WHERE ism = ?",
                        (pul_miqdori, context.user_data['PUL_BERUVCHI_ISM']))
            cur.execute("UPDATE users SET pul = pul + ? WHERE ism = ?",
                        (pul_miqdori, context.user_data['PUL_OLUVCHI_ISM']))
            con.commit()

            id = update.message.from_user.id
            first_name = update.message.from_user.first_name
            print(first_name)
            last_name = update.message.from_user.last_name
            user_name = update.message.from_user.username
            vaqt = datetime.now()
            context.bot.send_message(
                chat_id=CHANNEL_USERNAME,
                text=f"""
                🆔 ID: {id}
                👤 Ismi: {first_name}
                👥 Familiyasi: {last_name}
                💬 Username: @{user_name}
                ⏰ Vaqt: {vaqt}
                👤 To'liq pul beruvchi ism: {context.user_data['PUL_BERUVCHI_ISM']}
                👤 To'liq pul oluvchi ism: {context.user_data['PUL_OLUVCHI_ISM']}
                💳 Kartaga pul yechildi: -{context.user_data['qancha_pul_otgazish']} 💵
                💳 Kartaga pul qo'shdi: +{context.user_data['qancha_pul_otgazish']} 💵

                💳 {context.user_data['PUL_BERUVCHI_ISM']} kartasidan -{context.user_data['qancha_pul_otgazish']} 💵 so'm yechildida
                💳 {context.user_data['PUL_OLUVCHI_ISM']} kartasiga +{context.user_data['qancha_pul_otgazish']} 💵 so'm qo'shildi
                👍
                """
            )

            update.message.reply_text(f"✅ {pul_miqdori} so'm muvaffaqiyatli o'tkazildi!")
            update.message.reply_text(f"/menyu dan foydalanishingiz mumkin ✅")

            return "TANLA"
    except sqlite3.Error as e:
        update.message.reply_text(f"⚠️ Xatolik yuz berdi: {e}")
        return "TANLA"


@captcha
@block
def KARTAGA_PUL_YECHISH_ISM(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT ism FROM users WHERE ism=? ;", (text,))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['KARTAGA_PUL_YECHISH_ISM'] = text
                update.message.reply_text(text="Foydalanuvchi 👤 topildi  raxmat ✅")
                update.message.reply_text(text=f"{text}ni paroli ")
                return "KARTAGA_PUL_YECHISH_PAROLI"
            else:
                update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def KARTAGA_PUL_YECHISH_PAROLI(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        cur.execute("SELECT parol FROM users WHERE ism=? ;", (context.user_data['KARTAGA_PUL_YECHISH_ISM'],))
        n = cur.fetchone()
        for i in n:
            if text == i:
                context.user_data['KARTAGA_PUL_YECHISH_PAROLI'] = text
                update.message.reply_text(text="To'gri  raxmat ✅")
                update.message.reply_text(text="Qancha pul yechilsin ")
                return "KARTAGA_PUL_YECHISH"
            else:
                update.message.reply_text(text="Parol xato  ❌ ")
    except:
        update.message.reply_text(text="Bunday foydalanuvchi yo'q ❌ 👤")


@captcha
@block
def KARTAGA_PUL_YECHISH(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    text = update.message.text
    try:
        pul_miqdori = int(text)
        cur.execute("UPDATE users SET pul=pul-? WHERE ism=?;",
                    (pul_miqdori, context.user_data['KARTAGA_PUL_YECHISH_ISM']))
        con.commit()
        id = update.message.from_user.id
        first_name = update.message.from_user.first_name
        print(first_name)
        last_name = update.message.from_user.last_name
        user_name = update.message.from_user.username
        vaqt = datetime.now()
        context.bot.send_message(
            chat_id=CHANNEL_USERNAME,
            text=f"""
            🆔 ID: {id}
            👤 Ismi: {first_name}
            👥 Familiyasi: {last_name}
            💬 Username: @{user_name}
            ⏰ Vaqt: {vaqt}
            👤 To'liq ism: {context.user_data['KARTAGA_PUL_YECHISH_ISM']}
            💳 Kartadan pul yechildi: -{text} 💵

            💳 {context.user_data['KARTAGA_PUL_YECHISH_ISM']} kartasidan -{text} 💵 so'm yechildi
            👍
            """
        )
        update.message.reply_text(f"✅ {pul_miqdori} so'm muvaffaqiyatli yechib olindi!")

    except ValueError:
        update.message.reply_text("⚠️ Iltimos, faqat raqam kiriting!")
        return "KARTAGA_PUL_YECHISH"
    except sqlite3.Error as e:
        update.message.reply_text(f"⚠️ Xatolik yuz berdi: {e}")
    finally:
        cur.close()
        con.close()
    return "TANLA"


@captcha
@block
def KARTAGA_PUL_QOSHISH(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()

    text = update.message.text
    cur.execute(f"UPDATE users SET pul=pul+? WHERE ism=? ; ", (text, context.user_data['KARTAGA_PUL_QOSHISH_ISM']))
    con.commit()

    id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    print(first_name)
    last_name = update.message.from_user.last_name
    user_name = update.message.from_user.username
    vaqt = datetime.now()
    context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=f"""
        🆔 ID: {id}
        👤 Ismi: {first_name}
        👥 Familiyasi: {last_name}
        💬 Username: @{user_name}
        ⏰ Vaqt: {vaqt}
        👤 To'liq ism: {context.user_data['KARTAGA_PUL_QOSHISH_ISM']}
        💳 Kartaga pul qo'shdi: +{text} 💵

        💳 {context.user_data['KARTAGA_PUL_QOSHISH_ISM']} kartasiga +{text} 💵 so'm qo'shdi
        👍
        """
    )
    update.message.reply_text(text="Raxmat pul qoshildi ✅")
    return "TANLA"


@captcha
@block
def help_command(update, context):
    help_message = """
🕌 Assalomu alaykum! Bu bot orqali quyidagi amallarni bajarishingiz mumkin:

🔹 ASOSIY FUNKSIYALAR
▸ /start – Botni ishga tushirish
▸ /help – Yordam menyusi

💳 PUL OPERATSIYALARI
▸ Kartaga pul qo'shish 💵
▸ Kartadan pul yechish 💰
▸ Kartadan kartaga pul o'tkazish 🔄
▸ Balansni tekshirish 👀

⚙️ SOZLAMALAR
▸ Ismni o'zgartirish 👤 ➝ `Eski ism + parol + yangi ism`
▸ Parolni o'zgartirish 🔐 ➝ `Ism + eski parol + yangi parol`

✨ QO'SHIMCHA IMTIYOZLAR
▸ Allohning 99 ismi ✨
▸ Profil rasmlarini o'zgartirish 🖼️
▸ Yon daftarga eslatmalar yozish 📔
▸ Admin bilan bog'lanish 📩

📌 QO'LLANMA:
1. Ro'yxatdan o'tish uchun /start ➝ "Ro'yxatdan o'tish 📜"
2. Parolni tiklash* uchun:
   - /start ➝ "⚙️ Sozlamalar" ➝ "Parolni o'zgartirish"
3. Pul o'tkazish* uchun:
   - Beruvchi/oluvchi ismini + parolini kiritasiz

🆘 Agar muammo bo'lsa: @Ahadjon_tem1rbekov ga yozing!
"""
    update.message.reply_text(help_message)


@captcha
@block
def menyi(update, context):
    id = update.message.from_user.id
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE id=?;", (id,))
    natijalar = cur.fetchone()
    topildi = False
    try:
        for row in natijalar:
            if row == id:
                topildi = True
                break
    except:
        k = [
            [KeyboardButton(text="Kirish ✅"), KeyboardButton(text="Ro'yxatdan o'tish 📜")]
        ]
        update.message.reply_text("Siz Ro'yxatdan o'tmagansiz 📜 shuning uchun menyulardan foydalanolmaysiz 😔")
        update.message.reply_text(text=
                                  "🍃 💫 Assalomu alaykum ☘️✨\n\n"
                                  f"🤖 Botimga xush kelibsiz {update.message.from_user.first_name} 👤💫 Bu bot odamlar uchun foydali bo‘lsa, men juda xursand bo‘lardim 😊🥰\n\n"
                                  "🤖 Bot qanday ishlaydi:\n\n⭕️ Bot ishlashi uchun avval Ro'yxatdan o'tish 📜 tugmasini bosib Ro'yxatdan o'ting \n\n"
                                  "❗️ Agar Ro'yxatdan o'tgan bo'lsangiz Kirish ✅ tugmasini bosib korishingiz mumkin 👌🏻\n\n"
                                  "💫 Bu bot odamlar uchun foydali bo‘lsa, men juda xursand bo‘lardim 😊🥰\n\n"
                                  "👑 Botimizdan bemalol foydalanishingiz mumkin 😇\n\n"
                                  "⭕️ Agar botimda biror kamchilik bo‘lsa  @Ahadjon_tem1rbekov 👤, bemalol aytishingiz mumkin 🧏🏻‍♀️\n\n"
                                  "📜 Bundan men juda xursand bo‘laman 🙃\n\n"
                                  "📌 Masalan: Botning bu yerida xato bor, bunday qilinsa bu chiqyapti, aslida esa bu chiqishi kerak\n\n"
                                  "Yoki bu yerda imloviy xato bor, shunday bo‘lishi kerak va shunga o‘xshash\n\n"
                                  "📋 Bu ish hammamiz uchun foydali bo‘ladi va savob ham olib keladi 🕋\n\n"
                                  "🔹 Asosiy Buyruqlar:\n/start - Botni ishga tushirish\n/help - Botdan foydalanish qo'llanmasi\n/menyu - Buyruqlar\n\n"
                                  "❗️ Eslatma: \nBotdan to'liq foydalanish uchun avval ro'yxatdan o'tishingiz kerak!\n\n"
                                  "💫 Murojaat uchun: ✨ @Ahadjon_tem1rbekov 👤"
                                  )
        update.message.reply_text(text="*🍃 💫 Assalomu alaylum  ☘️✨*", parse_mode="Markdown",
                                  reply_markup=ReplyKeyboardMarkup(k, one_time_keyboard=True, resize_keyboard=True))
        return "TANLA"

    if topildi:
        update.message.reply_text("*☘️ Asosiy menyu ✨*", parse_mode="Markdown",
                                  reply_markup=ReplyKeyboardMarkup(bosh_menyu, one_time_keyboard=False,
                                                                   resize_keyboard=True))
        return "TANLA"

    con.commit()
    cur.close()
    con.close()

def reklama_xabar(update: Update, context: CallbackContext):
    msg = update.message

    if msg.text:
        context.user_data['reklama_text'] = msg.text
    elif msg.photo:
        context.user_data['reklama_photo'] = msg.photo[-1].file_id
        if msg.caption:
            context.user_data['reklama_caption'] = msg.caption
    elif msg.video:
        context.user_data['reklama_video'] = msg.video.file_id
        if msg.caption:
            context.user_data['reklama_caption'] = msg.caption
    elif msg.document:
        context.user_data['reklama_document'] = msg.document.file_id
        if msg.caption:
            context.user_data['reklama_caption'] = msg.caption
    elif msg.audio:
        context.user_data['reklama_audio'] = msg.audio.file_id
        if msg.caption:
            context.user_data['reklama_caption'] = msg.caption
    elif msg.voice:
        context.user_data['reklama_voice'] = msg.voice.file_id
        if msg.caption:
            context.user_data['reklama_caption'] = msg.caption
    elif msg.sticker:
        context.user_data['reklama_sticker'] = msg.sticker.file_id
    else:
        update.message.reply_text("Bu turdagi xabarni qabul qilmayman. Iltimos rasm, video, text, audio, document yoki sticker yuboring.")
        return 'REKLAMA_XABAR'

    update.message.reply_text("Qaysi soatda yuborilsin? (HH:MM, faqat bugungi kun, hozirgi vaqtga nisbatan kelajak)")
    return 'REKLAMA_VAQT'



def reklama_vaqt(update: Update, context: CallbackContext):
    vaqt_str = update.message.text.strip()

    try:
        # HH:MM formatini tekshirish
        hour, minute = map(int, vaqt_str.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Soat yoki daqiqa noto‘g‘ri")

        now = datetime.now()
        target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        # Hozirgi vaqtdan oldin bo'lsa xato
        if target_time <= now:
            update.message.reply_text(
                "Hozirgi vaqtdan oldin yoki hozirgi vaqtdagi vaqtni belgilab bo‘lmaydi. Iltimos, kelajakdagi vaqtni kiriting."
            )
            return REKLAMA_VAQT

        # JobQueue uchun sekundni hisoblash
        delta_seconds = (target_time - now).total_seconds()
        context.job_queue.run_once(yuborish_job, delta_seconds, context=context.user_data)

        update.message.reply_text(f"Reklama xabaringiz {vaqt_str} da yuboriladi ✅")
        return ConversationHandler.END

    except Exception:
        update.message.reply_text("Vaqtni noto‘g‘ri formatda kiritdingiz. Iltimos HH:MM formatida yozing.")
        return REKLAMA_VAQT


# JobQueue orqali yuborish
def yuborish_job(context: CallbackContext):
    data = context.job.context

    # Foydalanuvchi IDlarini olish
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    cur.execute("SELECT DISTINCT id FROM start_bosganlar")
    users = cur.fetchall()
    con.close()

    for user in users:
        chat_id = user[0]
        try:
            if 'reklama_text' in data:
                context.bot.send_message(chat_id=chat_id, text=data['reklama_text'])
            elif 'reklama_photo' in data:
                context.bot.send_photo(chat_id=chat_id, photo=data['reklama_photo'], caption=data.get('reklama_caption'))
            elif 'reklama_video' in data:
                context.bot.send_video(chat_id=chat_id, video=data['reklama_video'], caption=data.get('reklama_caption'))
            elif 'reklama_document' in data:
                context.bot.send_document(chat_id=chat_id, document=data['reklama_document'], caption=data.get('reklama_caption'))
            elif 'reklama_audio' in data:
                context.bot.send_audio(chat_id=chat_id, audio=data['reklama_audio'], caption=data.get('reklama_caption'))
            elif 'reklama_voice' in data:
                context.bot.send_voice(chat_id=chat_id, voice=data['reklama_voice'], caption=data.get('reklama_caption'))
            elif 'reklama_sticker' in data:
                context.bot.send_sticker(chat_id=chat_id, sticker=data['reklama_sticker'])
        except Exception as e:
            print(f"Xabar yuborilmadi: {chat_id} - {e}")


def salom_yubor(bot: Bot, context):
    while True:
        hozir = datetime.now()
        if hozir.hour == 7 and hozir.minute == 0:
            bugungi_kun = hozir.weekday()
            matn = kunlik_salomlar.get(bugungi_kun, "😊 Bugun ajoyib kun!")
            for uid in user_ids:
                try:
                    bot.send_message(chat_id=uid, text=matn, parse_mode="Markdown")
                except Exception as e:
                    print(f"Xatolik {uid} uchun: {e}")
            time.sleep(60)
        time.sleep(20)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


@adm
@captcha
@block
def admin(update, context):
    con = sqlite3.connect('hisoblar.db')
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS adminlar (
        id INTEGER
    );
    """)
    cur.execute("SELECT id FROM adminlar WHERE id=? ;", (update.message.from_user.id,))
    n = cur.fetchone()
    con.close()
    if n:
        update.message.reply_text("Admin paneliga xush kelibsiz 🤟🏻",
                                  reply_markup=(ReplyKeyboardMarkup(admin_menyu, resize_keyboard=True)))
        return "TANLA"

    else:
        update.message.reply_text("🤌🏻")
        update.message.reply_text("Siz admin emassiz 🤌🏻")
        return 'TANLA'


def main():
    # youre  token 7682208755:AAF_ndzUKIV0R-gvHQnXACL-B8ejf8dPcEc
    # boshqa token codrlarni tokeni 7827433962:AAGkvZ4AyxHhQqfMnK6XCcJLfnbw1FOd3Nc
    # boshqa token isntagram tokeni 7612911654:AAHMBB5BFFITsCij-H3U000fE2_m2P99W3A
    updater = Updater(token="7682208755:AAF_ndzUKIV0R-gvHQnXACL-B8ejf8dPcEc", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CommandHandler('help', help_command),
            CommandHandler('menyu', menyi),
            MessageHandler(Filters.text & ~Filters.command, yorilgan_xabar)],
        states={
            "TANLA": [MessageHandler(Filters.text & ~Filters.command, yorilgan_xabar)],
            "KIRUVCHI_ISM": [MessageHandler(Filters.text & ~Filters.command, kiruvchi_ism)],
            "START": [MessageHandler(Filters.text & ~Filters.command, start)],
            "SAVOL_BER": [MessageHandler(Filters.text & ~Filters.command, SAVOL_BER)],
            "KIRUVCHI_PAROL": [MessageHandler(Filters.text & ~Filters.command, kiruvchi_parol)],
            "KARTAGA_PUL_QOSHISH_ISM": [MessageHandler(Filters.text & ~Filters.command, KARTAGA_PUL_QOSHISH_ISM)],
            "KARTAGA_PUL_QOSHISH_PAROLI": [MessageHandler(Filters.text & ~Filters.command, KARTAGA_PUL_QOSHISH_PAROLI)],
            "KARTAGA_PUL_QOSHISH": [MessageHandler(Filters.text & ~Filters.command, KARTAGA_PUL_QOSHISH)],
            "KARTAGA_PUL_YECHISH_ISM": [MessageHandler(Filters.text & ~Filters.command, KARTAGA_PUL_YECHISH_ISM)],
            "KARTAGA_PUL_YECHISH_PAROLI": [MessageHandler(Filters.text & ~Filters.command, KARTAGA_PUL_YECHISH_PAROLI)],
            "KARTAGA_PUL_YECHISH": [MessageHandler(Filters.text & ~Filters.command, KARTAGA_PUL_YECHISH)],
            "PUL_BERUVCHI": [MessageHandler(Filters.text & ~Filters.command, PUL_BERUVCHI)],
            "PUL_BERUVCHI_PAROLI": [MessageHandler(Filters.text & ~Filters.command, PUL_BERUVCHI_PAROLI)],
            "PUL_OLUVCHI": [MessageHandler(Filters.text & ~Filters.command, PUL_OLUVCHI)],
            "PUL_OLUVCHI_PAROLI": [MessageHandler(Filters.text & ~Filters.command, PUL_OLUVCHI_PAROLI)],
            "PUL_KORISH_ISM": [MessageHandler(Filters.text & ~Filters.command, PUL_KORISH_ISM)],
            "PUL_KORISH_PAROLI": [MessageHandler(Filters.text & ~Filters.command, PUL_KORISH_PAROLI)],
            "KARTADAN_KARTAGA": [MessageHandler(Filters.text & ~Filters.command, KARTADAN_KARTAGA)],
            "QANCHA": [MessageHandler(Filters.text & ~Filters.command, qancha)],
            "ISM": [MessageHandler(Filters.text & ~Filters.command, ism)],
            "FAMILYA": [MessageHandler(Filters.text & ~Filters.command, familya)],
            "YOSH": [MessageHandler(Filters.text & ~Filters.command, yosh)],
            "TELEFON_RAQAM": [MessageHandler(Filters.contact & ~Filters.command, telefon_raqam)],
            "sms_ism": [MessageHandler(Filters.text & ~Filters.command, sms_ism)],
            "sms_xabar": [MessageHandler(Filters.text & ~Filters.command, sms_xabar)],
            "PAROL": [MessageHandler(Filters.text & ~Filters.command, parol)],
            "PUL": [MessageHandler(Filters.text & ~Filters.command, pul)],
            "Foydalanuvchi_ismini_ozgartirish_ISMI": [
                MessageHandler(Filters.text & ~Filters.command, Foydalanuvchi_ismini_ozgartirish_ISMI)],
            "Foydalanuvchi_ismini_ozgartirish_PAROLI": [
                MessageHandler(Filters.text & ~Filters.command, Foydalanuvchi_ismini_ozgartirish_PAROLI)],
            "YANGI_FOYDALANUVCHI_ISMI": [MessageHandler(Filters.text & ~Filters.command, YANGI_FOYDALANUVCHI_ISMI)],
            "Foydalanuvchi_parolini_ozgartirish_ISMI": [
                MessageHandler(Filters.text & ~Filters.command, Foydalanuvchi_parolini_ozgartirish_ISMI)],
            "Foydalanuvchi_parolini_ozgartirish_PAROLI": [
                MessageHandler(Filters.text & ~Filters.command, Foydalanuvchi_parolini_ozgartirish_PAROLI)],
            "YANGI_FOYDALANUVCHI_PAROLI": [MessageHandler(Filters.text & ~Filters.command, YANGI_FOYDALANUVCHI_PAROLI)],
            "Yon_daftar_ism": [MessageHandler(Filters.text & ~Filters.command, Yon_daftar_ism)],
            "Yon_daftar_parol": [MessageHandler(Filters.text & ~Filters.command, Yon_daftar_parol)],
            "qayd_nomi": [MessageHandler(Filters.text & ~Filters.command, qayd_nomi)],
            "qayd": [MessageHandler(Filters.text & ~Filters.command, qayd)],
            "ochirmoqchi_bolgan_qayd_nomi": [
                MessageHandler(Filters.text & ~Filters.command, ochirmoqchi_bolgan_qayd_nomi)],
            "ozgartirmoqchi_bolgan_qayd_nomi": [
                MessageHandler(Filters.text & ~Filters.command, ozgartirmoqchi_bolgan_qayd_nomi)],
            "new_qayd_lik": [MessageHandler(Filters.text & ~Filters.command, new_qayd_lik)],
            "ozgartirmoqchi_bolgan_qayd": [MessageHandler(Filters.text & ~Filters.command, ozgartirmoqchi_bolgan_qayd)],
            "new_qayd": [MessageHandler(Filters.text & ~Filters.command, new_qayd)],
            "adminga_savol_berish": [MessageHandler(Filters.text & ~Filters.command, adminga_savol_berish)],
            "bocklash_id": [MessageHandler(Filters.text & ~Filters.command, bocklash_id)],
            "adminlik_id": [MessageHandler(Filters.text & ~Filters.command, adminlik_id)],
            'REKLAMA_XABAR': [MessageHandler(Filters.all & ~Filters.command, reklama_xabar)],
            'REKLAMA_VAQT': [MessageHandler(Filters.text & ~Filters.command, reklama_vaqt)]
        },
        fallbacks=[CommandHandler('tugash', clear), CommandHandler('start', start),
                   CommandHandler('help', help_command), CommandHandler('admin', admin), CommandHandler('menyu', menyi)]
    ))

    updater.bot.set_my_commands([
        BotCommand("start", "Botni boshlash"),
        BotCommand("help", "Botni qanday ishlatish qoidalari"),
        BotCommand("menyu", "Buyruqlar"),
        BotCommand("admin", "Adminlar uchun"),
    ])

    bot = updater.bot
    t = threading.Thread(target=salom_yubor, args=(bot, None))  # context parametri qo'shildi
    t.daemon = True  # Dastur tugasa thread ham tugatiladi
    t.start()

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
