import os
import logging
import psycopg2  # <-- PostgreSQL bilan ishlash uchun
from datetime import datetime, timedelta, time
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackContext
)

from images_paths import images_paths
from recipes_texts import recipes_texts
from diseases_data import diseases_data

# ============== LOGGER (log) sozlamalari ==============
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============== ADMIN IDs: Siz bu yerga o‘z ID raqamingizni yozasiz ==============
ADMIN_IDS = [7465094605]  # <-- O'zingizning telegram ID raqamingizni yozing

# ============== TOKEN (o'zingizning BOT_TOKEN ni kiriting) ==============
BOT_TOKEN = "7904798084:AAFrf5U2QcZ4zJRFi8CQ6wtWHAA172K9AJ4"  # <-- Bot tokeningizni yozing

# ============== PostgreSQL ulanish parametrlari ==============
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "1212"

# --- Bu yerni o'zingizga moslang ---

# -- yoki shunday ham qilishingiz mumkin (bitta DSN qatorda):
# DATABASE_URL = "postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/my_telegram_bot_db"

# Keling, oddiy usulda alohida funksiyalar yozamiz:
def get_connection():
    """
    PostgreSQL bilan ulanish o'rnatish uchun yordamchi funksiya.
    Har safar chaqirib, ish bitgach `conn.close()` qilish tavsiya etiladi
    (yoki 'with' context manager bilan).
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# ============== BAZA bilan ishlashga oid yordamchi funksiyalar ==============

def create_or_update_user(user_id: int, age=None, height=None, weight=None):
    """
    Agar user users jadvalida mavjud bo'lmasa, qo'shadi.
    Agar mavjud bo'lsa va age/height/weight berilgan bo'lsa - yangilaydi.
    Har safar last_activity ni ham yangilab boradi.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # Avval tekshiramiz user mavjudmi:
                cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
                result = cur.fetchone()
                now_str = datetime.now()
                if result is None:
                    # Insert
                    cur.execute(
                        """
                        INSERT INTO users (user_id, age, height, weight, last_activity, registered_time)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (user_id, age, height, weight, now_str, now_str)
                    )
                else:
                    # Update
                    # Faqat berilgan qiymatlar update qilinadi:
                    if age is not None:
                        cur.execute("UPDATE users SET age=%s WHERE user_id=%s", (age, user_id))
                    if height is not None:
                        cur.execute("UPDATE users SET height=%s WHERE user_id=%s", (height, user_id))
                    if weight is not None:
                        cur.execute("UPDATE users SET weight=%s WHERE user_id=%s", (weight, user_id))
                    # last_activity har doim update
                    cur.execute("UPDATE users SET last_activity=%s WHERE user_id=%s", (now_str, user_id))
    finally:
        conn.close()


def get_user_info(user_id: int):
    """
    users jadvalidan ma'lumotni qaytaradi (lug'at ko‘rinishida).
    Bo'lmasa None qaytaradi.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT user_id, age, height, weight, last_activity, registered_time
                    FROM users
                    WHERE user_id = %s
                """, (user_id,))
                row = cur.fetchone()
                if row is None:
                    return None
                # row = (user_id, age, height, weight, last_activity, registered_time)
                return {
                    "user_id": row[0],
                    "age": row[1],
                    "height": row[2],
                    "weight": row[3],
                    "last_activity": row[4],
                    "registered_time": row[5]
                }
    finally:
        conn.close()

def delete_user(user_id: int):
    """
    Foydalanuvchini bazadan o'chirib tashlaydi.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    finally:
        conn.close()

def update_user_last_activity(user_id: int):
    """
    Foydalanuvchining so'nggi faoliyat vaqtini yangilab qo'yadi.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                now_str = datetime.now()
                cur.execute("UPDATE users SET last_activity=%s WHERE user_id=%s", (now_str, user_id))
    finally:
        conn.close()

# -- last_main_menu jadvali bilan ishlash:
def set_user_last_main_menu(user_id: int, message_id: int):
    """
    user_last_main_menu jadvalida (user_id, message_id) saqlash yoki update qilish.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM user_last_main_menu WHERE user_id=%s", (user_id,))
                res = cur.fetchone()
                if res is None:
                    # insert
                    cur.execute("""
                        INSERT INTO user_last_main_menu (user_id, message_id)
                        VALUES (%s, %s)
                    """, (user_id, message_id))
                else:
                    # update
                    cur.execute("""
                        UPDATE user_last_main_menu
                        SET message_id=%s
                        WHERE user_id=%s
                    """, (message_id, user_id))
    finally:
        conn.close()

def get_user_last_main_menu(user_id: int):
    """
    user_last_main_menu jadvalidan message_id ni qaytaradi.
    Bo'lmasa None
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT message_id FROM user_last_main_menu WHERE user_id=%s", (user_id,))
                row = cur.fetchone()
                if row:
                    return row[0]
                return None
    finally:
        conn.close()

def delete_user_last_main_menu(user_id: int):
    """
    user_last_main_menu jadvalidan ma'lumotni o'chiradi.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM user_last_main_menu WHERE user_id=%s", (user_id,))
    finally:
        conn.close()


# -- Broadcastlar bilan ishlash:
def create_broadcast(admin_id: int) -> int:
    """
    broadcasts jadvaliga yangi qator qo'shib, yangi broadcast_id ni qaytaradi.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO broadcasts (admin_id) VALUES (%s)
                    RETURNING broadcast_id
                    """,
                    (admin_id,)
                )
                new_broadcast_id = cur.fetchone()[0]
                return new_broadcast_id
    finally:
        conn.close()

def add_broadcast_message(broadcast_id: int, chat_id: int, message_id: int):
    """
    broadcast_messages jadvaliga ma'lumot qo'shish.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO broadcast_messages (broadcast_id, chat_id, message_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (broadcast_id, chat_id)
                    DO UPDATE SET message_id = EXCLUDED.message_id
                    """,
                    (broadcast_id, chat_id, message_id)
                )
    finally:
        conn.close()

def get_broadcast_messages(broadcast_id: int):
    """
    Ma'lum broadcast_id bo'yicha chat_id va message_id ro'yxatini qaytaradi.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT chat_id, message_id
                    FROM broadcast_messages
                    WHERE broadcast_id = %s
                    """,
                    (broadcast_id,)
                )
                rows = cur.fetchall()
                # [(chat_id, message_id), (chat_id, message_id), ...]
                return rows
    finally:
        conn.close()

def delete_broadcast(broadcast_id: int):
    """
    broadcasts jadvalidan broadcast_id ni (va unga bog'liq broadcast_messages ni) o'chiradi.
    """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # broadcast_messages da ON DELETE CASCADE bo'lgani uchun broadcasts dagi qator o'chsa
                # unga bog'liq barcha broadcast_messages ham o'chadi.
                cur.execute("DELETE FROM broadcasts WHERE broadcast_id = %s", (broadcast_id,))
    finally:
        conn.close()

def edit_broadcast_messages(broadcast_id: int, new_text: str, context: CallbackContext):
    """
    Ushbu funktsiya broadcast_id bo'yicha yuborilgan xabarlarni topib, ularning matnini yangilaydi.
    (Admin buyruqlari bo'yicha ishlatiladi)
    """
    rows = get_broadcast_messages(broadcast_id)
    edit_count = 0
    fail_count = 0
    for (chat_id, msg_id) in rows:
        try:
            context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=new_text
            )
            edit_count += 1
        except Exception as e:
            logger.error(f"Edit failed for chat {chat_id}, msg {msg_id}: {e}")
            fail_count += 1
    return edit_count, fail_count


# ============== Yordamchi funksiya: uzun matnni bo‘lib yuborish ==============
async def send_long_text_in_chunks(text, chat_id, context, chunk_size=3500):
    """
    Telegram cheklovi sababli xabarni 4096 belgidan katta yuborolmaymiz.
    Xavfsiz tomoni uchun 3500 belgi atrofida bo'lib yuboriladi.
    """
    start = 0
    last_text_id = None
    while start < len(text):
        end = start + chunk_size
        sent_message = await context.bot.send_message(chat_id=chat_id, text=text[start:end])
        last_text_id = sent_message.message_id
        start = end
    return last_text_id

# ============== KUNLIK ESLATMA (JobQueue) ==============
async def daily_reminder_job(context: CallbackContext):
    """
    Har kuni foydalanuvchining ro'yxatdan o'tgan vaqtida ishga tushadigan job.
    Foydalanuvchiga Ha/Yo'q tugmalari bilan eslatma yuboradi.
    Agar botni bloklagan bo‘lsa — bazadan o‘chirib tashlaymiz.
    """
    job_data = context.job.data  # {"chat_id": int(uid_str), "uid_str": uid_str}
    chat_id = job_data["chat_id"]

    user_info = get_user_info(chat_id)
    if not user_info:
        # Agar bazada user yo'q bo'lib qolgan bo'lsa, job ni ham bekor qilamiz:
        context.job.schedule_removal()
        return

    # Xabar matnini tayyorlaymiz
    reminder_text = (
        "Bugungi tavsiyalar:\n"
        "1) Tanlagan sport mashg'ulotingizni bajarishni unutmang!\n"
        "2) Ko'proq suv ichish, sabzavot va meva iste'mol qiling.\n"
        "3) Shirin, gazlangan, spirtli ichimliklar va boshqa zararli odatlardan uzoq bo'ling.\n"
        "4) Kunlik suv iste'moli: O'rtacha 2-3 litr.\n\n"
        "Ushbu tavsiyalarga amal qildingizmi?"
    )

    keyboard = [
        [
            InlineKeyboardButton("Ha ✅", callback_data="daily_yes"),
            InlineKeyboardButton("Yo'q ❌", callback_data="daily_no")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await context.bot.send_message(chat_id=chat_id, text=reminder_text, reply_markup=reply_markup)
    except Exception as e:
        logger.warning(f"User {chat_id} blocked the bot or another error: {e}")
        delete_user(chat_id)  # bazadan o'chirib tashlaymiz
        context.job.schedule_removal()

def schedule_user_reminder(application, user_id: int, reg_dt: datetime):
    """
    Foydalanuvchini ertangi kundan boshlab, har kuni ayni soat/minutda eslatma yuborish uchun job qo'yadi.
    """
    hr = reg_dt.hour
    mn = reg_dt.minute

    application.job_queue.run_daily(
        callback=daily_reminder_job,
        time=time(hour=hr, minute=mn),
        days=(0, 1, 2, 3, 4, 5, 6),
        name=f"daily_reminder_{user_id}",
        data={"chat_id": user_id}
    )

async def daily_reminder_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Kunlik eslatma Ha/Yo'q tugmalariga javob.
    """
    query = update.callback_query
    await query.answer()
    answer = query.data.split('_')[1]  # 'yes' yoki 'no'

    if answer == 'yes':
        text = (
            "Barakalla! 👏\n"
            "Kunlik rejalaringizga amal qilganingiz uchun sizga rahmat.\n"
            "Yana shu ruhda davom eting! 💪\n"
            "Quyidagi o'zingizga kerakli bo'limlardan birini tanlang."
        )
    else:
        text = (
            "Hali kech emas! 😇\n"
            "Tavsiyalarni bajarsangiz, sog'lug'ingiz mustahkam bo'ladi.\n"
            "Hozirdan boshlang, ertangi kun albatta muvaffaqiyatli o'tadi! 💫\n"
            "Quyidagi o'zingizga kerakli bo'limlardan birini tanlang."
        )

    keyboard = [
        [InlineKeyboardButton("Taomlar 🍽", callback_data='main_taomlar')],
        [InlineKeyboardButton("Mashg'ulotlar 🏋️", callback_data='main_mashgulotlar')],
        [InlineKeyboardButton("Davolanish 🏥", callback_data='main_davolanish')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=text, reply_markup=reply_markup)

# ============== /start KOMANDASI ==============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_info = get_user_info(chat_id)
    if user_info is None:
        # Bu user bazada yo'q -- yangi user
        create_or_update_user(chat_id, age=None, height=None, weight=None)
        reg_dt = datetime.now()
        schedule_user_reminder(context.application, chat_id, reg_dt)
    else:
        # Mavjud bo'lsa faqat last_activity yangilash
        update_user_last_activity(chat_id)

    text = (
        "Assalomu alaykum!☺️ Sog'lom turmush tarzini targ'ib qiluvchi botga xush kelibsiz!\n"
        "Yoshingiz, bo'yingiz (sm) va vazningizni (kg) kiriting (masalan: 25, 175, 70)."
    )
    await context.bot.send_message(chat_id=chat_id, text=text)

# ============== FOYDALANUVCHI MA'LUMOTLARINI QABUL QILISH (TEXT) ==============
async def handle_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    update_user_last_activity(user_id)

    user_info = get_user_info(user_id)
    if user_info is None:
        # Avval /start bosilmagan yoki bazada user yo'q
        create_or_update_user(user_id)
        await update.message.reply_text("Iltimos, avval /start ni bosing.")
        return

    try:
        age, height, weight = map(int, update.message.text.replace(' ', '').split(','))
        create_or_update_user(user_id, age=age, height=height, weight=weight)

        height_m = height / 100
        bmi = weight / (height_m ** 2)
        # BMR ni ham oddiy formula bilan
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
        daily_water_liters = weight * 30 / 1000

        if bmi < 18.5:
            bmi_status = "Sizning vazningiz kam. Vazn olish tavsiya etiladi.🙂"
        elif 18.5 <= bmi < 24.9:
            bmi_status = "Sizning vazningiz sog'lom darajada.☺️"
        elif 25 <= bmi < 29.9:
            bmi_status = "Sizning vazningiz yuqori. Vazn yo'qotish tavsiya etiladi.🙃"
        else:
            bmi_status = "Sizda ortiqcha vazn bor. Mutaxassisga murojaat qiling.😌"

        summary_text = (
            f"Sizning BMI: 😊{bmi:.2f}. {bmi_status}\n"
            f"Kunlik kaloriya ehtiyojingiz (BMR): {bmr:.2f} kkal.\n"
            f"Kunlik suv iste'moli: {daily_water_liters:.1f} litr.\n\n"
            f"Zararli ichimlik va taomlardan saqlaning:\n"
            f"- Shirin gazlangan ichimliklar\n"
            f"- Spirtli ichimliklar\n"
            f"- Juda yog'li va qovurilgan ovqatlar\n"
            f"- Ortiqcha tuz va shakar\n\n"
            f"Foydali odatlar:\n"
            f"- Oddiy suv ichish\n"
            f"- Ko'katlar va mevalar\n"
            f"- Sog'lom yog'lar (zaytun moyi, urug' moylari)\n"
            "👉 @hayot_balansi 👈\n"
        )

        if len(summary_text) > 3500:
            await send_long_text_in_chunks(summary_text, update.effective_chat.id, context)
        else:
            await update.message.reply_text(summary_text)

        main_menu_text = "Quyidagilardan birini tanlang:"
        main_menu_keyboard = [
            [InlineKeyboardButton("Taomlar 🍽", callback_data='main_taomlar')],
            [InlineKeyboardButton("Mashg'ulotlar 🏋️", callback_data='main_mashgulotlar')],
            [InlineKeyboardButton("Davolanish 🏥", callback_data='main_davolanish')]
        ]
        sent_msg = await update.message.reply_text(main_menu_text, reply_markup=InlineKeyboardMarkup(main_menu_keyboard))

        # So'nggi asosiy menyu xabarini bazaga yozamiz:
        set_user_last_main_menu(user_id, sent_msg.message_id)

    except ValueError:
        await update.message.reply_text("Format xato. (Misol: 25, 175, 70).")

# ============== "recipes" tugmasi (Kunlik eslatma) ==============
async def recipes_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    update_user_last_activity(user_id)
    query = update.callback_query
    await query.answer()
    await show_main_taomlar_menu(update, context)

# ============== ASOSIY TAOMLAR MENYUSI ==============
async def show_main_taomlar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    text_label = "Taomlar bo‘limi. Qaysi bo‘limni tanlaysiz?"
    keyboard = [
        [InlineKeyboardButton("Suyuq taomlar🍲", callback_data='cat_suyuq')],
        [InlineKeyboardButton("Quyuq taomlar🍝", callback_data='cat_quyuq')],
        [InlineKeyboardButton("Salatlar🥗", callback_data='cat_salatlar')],
        [InlineKeyboardButton("Pishiriqlar🥧", callback_data='cat_pishiriqlar')],
        [InlineKeyboardButton("Shirinliklar🍩", callback_data='cat_shirinliklar')],
        [InlineKeyboardButton("Ichimliklar🍹", callback_data='cat_ichimliklar')],
        [InlineKeyboardButton("Tortlar🍰", callback_data='cat_tortlar')],
        [InlineKeyboardButton("Nonlar🍞", callback_data='cat_nonlar')],
        [InlineKeyboardButton("Ortga⬅️", callback_data='postcalc_back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text_label, reply_markup=reply_markup)

async def show_dish_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    update_user_last_activity(user_id)
    query = update.callback_query
    await query.answer()
    cat = query.data.split('_')[1]
    await show_dish_categories_logic(cat, query, context)

async def show_dish_categories_logic(cat: str, query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE):
    text_label = ""
    keyboard = []

    if cat == "suyuq":
        text_label = "Suyuq taomlar:🍲"
        keyboard = [
            [InlineKeyboardButton("Ko'za sho'rva", callback_data='dish_kosashorva')],
            [InlineKeyboardButton("Dumbulli dimlama", callback_data='dish_dumbullidimlama')],
            [InlineKeyboardButton("Piyozli sho'rva", callback_data='dish_piyozlishorva')],
            [InlineKeyboardButton("Suyuq norin", callback_data='dish_suyuqnorin')],
            [InlineKeyboardButton("Uyg'ur lag'mon", callback_data='dish_uygurlagmon')],
            [InlineKeyboardButton("Moxora", callback_data='dish_moxora')],
            [InlineKeyboardButton("Go'ja", callback_data='dish_goja')],
            [InlineKeyboardButton("Lag'mon", callback_data='dish_lagmon')],
            [InlineKeyboardButton("Sabzavotli do'lma", callback_data='dish_sabzavotd')],
            [InlineKeyboardButton("Mantili sho'rva", callback_data='dish_mantilishorva')],
            [InlineKeyboardButton("Firkadelkali sho'rva", callback_data='dish_firkadelkali')],
            [InlineKeyboardButton("Kosa dimlama", callback_data='dish_kosadimlama')],
            [InlineKeyboardButton("Tuxum do'lma", callback_data='dish_tuxumdolma')],
            [InlineKeyboardButton("Mastava", callback_data='dish_mastava')],
            [InlineKeyboardButton("Chuchvara", callback_data='dish_chuchvara')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "quyuq":
        text_label = "Quyuq taomlar:🍝"
        keyboard = [
            [InlineKeyboardButton("Andijon manti", callback_data='dish_andijonmanti')],
            [InlineKeyboardButton("Spagetti", callback_data='dish_spagetti')],
            [InlineKeyboardButton("Qovurma lag'mon", callback_data='dish_qovurmala')],
            [InlineKeyboardButton("Dimlama", callback_data='dish_dimlama')],
            [InlineKeyboardButton("Besh barmoq", callback_data='dish_beshbarmoq')],
            [InlineKeyboardButton("Bibimbap", callback_data='dish_bibimbap')],
            [InlineKeyboardButton("Do'lma", callback_data='dish_quyuqdolma')],
            [InlineKeyboardButton("Choyxona palov", callback_data='dish_choyxona')],
            [InlineKeyboardButton("Gulxonim", callback_data='dish_gulxonim')],
            [InlineKeyboardButton("Bayramona osh va ayron", callback_data='dish_bayramona')],
            [InlineKeyboardButton("Grechka palov", callback_data='dish_grechkapalov')],
            [InlineKeyboardButton("Turkcha ratatuy", callback_data='dish_turkcharatatuy')],
            [InlineKeyboardButton("Balish", callback_data='dish_balish')],
            [InlineKeyboardButton("Go'shli rulet", callback_data='dish_goshlirulet')],
            [InlineKeyboardButton("Shivit oshi", callback_data='dish_shivit')],
            [InlineKeyboardButton("Non palov", callback_data='dish_nonpalov')],
            [InlineKeyboardButton("Kartoshka do'lma", callback_data='dish_kartoshkadolma')],
            [InlineKeyboardButton("Dumbul palov", callback_data='dish_dumbulpalov')],
            [InlineKeyboardButton("Teftel", callback_data='dish_teftel')],
            [InlineKeyboardButton("Sarimsoqli kartoshka", callback_data='dish_sarimsoqli')],
            [InlineKeyboardButton("Begodi", callback_data='dish_begodi')],
            [InlineKeyboardButton("Baliqli kotlet", callback_data='dish_baliqlikotlet')],
            [InlineKeyboardButton("Jigar kabob", callback_data='dish_jigarkabob')],
            [InlineKeyboardButton("Qozon kabob", callback_data='dish_qozonkabob')],
            [InlineKeyboardButton("Qiymali kabob", callback_data='dish_qiymalikabob')],
            [InlineKeyboardButton("Tandir kabob", callback_data='dish_tandirkabob')],
            [InlineKeyboardButton("Tovuq kabob", callback_data='dish_tovuqkabob')],
            [InlineKeyboardButton("Namangan kabob", callback_data='dish_namangankabob')],
            [InlineKeyboardButton("Norin", callback_data='dish_norin')],
            [InlineKeyboardButton("Xasip", callback_data='dish_xasip')],
            [InlineKeyboardButton("Tuxum Barak", callback_data='dish_tuxumbarak')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "salatlar":
        text_label = "Salatlar:🥗"
        keyboard = [
            [InlineKeyboardButton("Achchiq chuchuk salat", callback_data='dish_achchiqchuchuk')],
            [InlineKeyboardButton("Bodring va brinzali salat", callback_data='dish_bodringbrinza')],
            [InlineKeyboardButton("Karam va pomidorli salat", callback_data='dish_karampomidor')],
            [InlineKeyboardButton("Gruzincha salat", callback_data='dish_gruzincha')],
            [InlineKeyboardButton("Qarsildoq salat", callback_data='dish_qarsildoq')],
            [InlineKeyboardButton("Suzmali salat", callback_data='dish_suzmali')],
            [InlineKeyboardButton("Penchuza salat", callback_data='dish_penchuza')],
            [InlineKeyboardButton("Mandarin salat", callback_data='dish_mandarin')],
            [InlineKeyboardButton("Tovuqli salat", callback_data='dish_tovuqlisalat')],
            [InlineKeyboardButton("Smak salat", callback_data='dish_smak')],
            [InlineKeyboardButton("Ozdiruvchi salat", callback_data='dish_ozdiruvchi')],
            [InlineKeyboardButton("Mevali salat", callback_data='dish_mevali')],
            [InlineKeyboardButton("Braslet salat", callback_data='dish_braslet')],
            [InlineKeyboardButton("Qotgan nonli salat", callback_data='dish_qotgannonli')],
            [InlineKeyboardButton("Go'shtli salat", callback_data='dish_goshtlisa')],
            [InlineKeyboardButton("Karamli salat", callback_data='dish_karamli')],
            [InlineKeyboardButton("Olivye", callback_data='dish_olivye')],
            [InlineKeyboardButton("Tovuqli olivye", callback_data='dish_tovuqiolivye')],
            [InlineKeyboardButton("Bodring salat", callback_data='dish_bodringsalat')],
            [InlineKeyboardButton("Shanxaycha salat", callback_data='dish_shanxay')],
            [InlineKeyboardButton("Qush uyali salat", callback_data='dish_qushuyali')],
            [InlineKeyboardButton("Toshkentcha salat", callback_data='dish_toshkentsalat')],
            [InlineKeyboardButton("Portobello salat", callback_data='dish_portobello')],
            [InlineKeyboardButton("Ananas va tovuqli salat", callback_data='dish_ananas')],
            [InlineKeyboardButton("Sezar salat", callback_data='dish_sezar')],
            [InlineKeyboardButton("Bodring va karamli salat", callback_data='dish_bodringkaram')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "pishiriqlar":
        text_label = "Pishiriqlar:🥧"
        keyboard = [
            [InlineKeyboardButton("Turkcha burek", callback_data='dish_turkchaburek')],
            [InlineKeyboardButton("Go’shtli somsa", callback_data='dish_goshtlisomsa')],
            [InlineKeyboardButton("Yupqa", callback_data='dish_yupqa')],
            [InlineKeyboardButton("Qiymali quymoq", callback_data='dish_qiymaliquymoq')],
            [InlineKeyboardButton("Pishloqli cheburek", callback_data='dish_pishloqlicheburek')],
            [InlineKeyboardButton("Gumma", callback_data='dish_gumma')],
            [InlineKeyboardButton("Pahlava", callback_data='dish_pahlava')],
            [InlineKeyboardButton("Chak-chak", callback_data='dish_chakchak')],
            [InlineKeyboardButton("Turkcha pishiriq", callback_data='dish_turkchapishiriq')],
            [InlineKeyboardButton("Qozon somsa", callback_data='dish_qozonsomsa')],
            [InlineKeyboardButton("Sabzavotli somsa", callback_data='dish_sabzavotlisomsa')],
            [InlineKeyboardButton("Yurak somsa", callback_data='dish_yuraksomsa')],
            [InlineKeyboardButton("Qatlama somsa", callback_data='dish_qatlamasomsa')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "shirinliklar":
        text_label = "Shirinliklar:🍩"
        keyboard = [
            [InlineKeyboardButton("Nisholda", callback_data='dish_nisholda')],
            [InlineKeyboardButton("Holvetar", callback_data='dish_holvetar')],
            [InlineKeyboardButton("Tvarogli krendel", callback_data='dish_tvaroglikr')],
            [InlineKeyboardButton("Shokoladli glazur", callback_data='dish_shokoglazur')],
            [InlineKeyboardButton("Bananli eskimo", callback_data='dish_bananlieskimo')],
            [InlineKeyboardButton("Jemli pirog", callback_data='dish_jemlipirog')],
            [InlineKeyboardButton("Tvarogli bulochka", callback_data='dish_tvoroglibulochka')],
            [InlineKeyboardButton("Malinali chizkeyk", callback_data='dish_malinalichizkeyk')],
            [InlineKeyboardButton("Bolqaymoq", callback_data='dish_bolqaymoq')],
            [InlineKeyboardButton("Murabboli pirog", callback_data='dish_murabbolipirog')],
            [InlineKeyboardButton("Asalli pirojniy", callback_data='dish_asallipirojniy')],
            [InlineKeyboardButton("Shaftolili muzqaymoq", callback_data='dish_shaftolilimizq')],
            [InlineKeyboardButton("Aylanay pirogi", callback_data='dish_aylanay')],
            [InlineKeyboardButton("Chumoli uyasi", callback_data='dish_chumoliuya')],
            [InlineKeyboardButton("Olchali pirog", callback_data='dish_olchali')],
            [InlineKeyboardButton("Shokoladli keks", callback_data='dish_shokokeks')],
            [InlineKeyboardButton("Asalli pechenye", callback_data='dish_asallipechenye')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "ichimliklar":
        text_label = "Ichimliklar:🍹"
        keyboard = [
            [InlineKeyboardButton("Olmali choy", callback_data='drink_olmali')],
            [InlineKeyboardButton("Namatak sharbati", callback_data='drink_namatak')],
            [InlineKeyboardButton("Yalpizli limon choy", callback_data='drink_yalpizlimon')],
            [InlineKeyboardButton("Qulupnayli ichimlik", callback_data='drink_qulupnay')],
            [InlineKeyboardButton("Qovun sharbati", callback_data='drink_qovun')],
            [InlineKeyboardButton("Bodomli sut", callback_data='drink_bodomli')],
            [InlineKeyboardButton("Uzum sharbati", callback_data='drink_uzum')],
            [InlineKeyboardButton("Mevali sharbat", callback_data='drink_mevali')],
            [InlineKeyboardButton("Qatiq", callback_data='drink_qatiq')],
            [InlineKeyboardButton("Tarvuz sharbati", callback_data='drink_tarvuz')],
            [InlineKeyboardButton("Sabzi sharbati", callback_data='drink_sabzi')],
            [InlineKeyboardButton("Zira choy", callback_data='drink_zira')],
            [InlineKeyboardButton("Vitaminli ichimlik", callback_data='drink_vitaminli')],
            [InlineKeyboardButton("Moxito", callback_data='drink_moxito')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "tortlar":
        text_label = "Tortlar:🍰"
        keyboard = [
            [InlineKeyboardButton("Praga torti", callback_data='tort_praga')],
            [InlineKeyboardButton("Napaleon torti", callback_data='tort_napaleon')],
            [InlineKeyboardButton("Zebra torti", callback_data='tort_zebra')],
            [InlineKeyboardButton("Pancho torti", callback_data='tort_pancho')],
            [InlineKeyboardButton("Medovik torti", callback_data='tort_medovik')],
            [InlineKeyboardButton("Frezye torti", callback_data='tort_frezye')],
            [InlineKeyboardButton("Karamel va yong’oqli tort", callback_data='tort_karamel')],
            [InlineKeyboardButton("Kita-kat torti", callback_data='tort_kitakat')],
            [InlineKeyboardButton("Bostoncha kremli tort", callback_data='tort_boston')],
            [InlineKeyboardButton("Bounty torti", callback_data='tort_bounty')],
            [InlineKeyboardButton("Pavlova torti", callback_data='tort_pavlova')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    elif cat == "nonlar":
        text_label = "Nonlar:🍞"
        keyboard = [
            [InlineKeyboardButton("Qatlama patir", callback_data='non_qatlamapatir')],
            [InlineKeyboardButton("Shirin kulcha", callback_data='non_shirinkulcha')],
            [InlineKeyboardButton("Moychechak non", callback_data='non_moychechak')],
            [InlineKeyboardButton("Go’shtli non", callback_data='non_goshtli')],
            [InlineKeyboardButton("Patir", callback_data='non_patir')],
            [InlineKeyboardButton("Lochira patir", callback_data='non_lochira')],
            [InlineKeyboardButton("Obi non", callback_data='non_obinon')],
            [InlineKeyboardButton("Qatlama", callback_data='non_qatlama')],
            [InlineKeyboardButton("Jizzali patir", callback_data='non_jizzali')],
            [InlineKeyboardButton("Ortga⬅️ ", callback_data='back_to_taomlar')]
        ]
    else:
        text_label = "Noma'lum bo‘lim."
        keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data='back_to_taomlar')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text_label, reply_markup=reply_markup)

# ============== Retsept callback: dish_..., drink_..., tort_..., non_, ... (ESKI KOD) ==============
async def show_recipe_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    update_user_last_activity(user_id)
    query = update.callback_query
    await query.answer()
    data_key = query.data
    text_data = recipes_texts.get(data_key, "Bu taom (yoki ichimlik) bo'yicha ma'lumot topilmadi.")
    image_path = images_paths.get(data_key)
    keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data='back_to_taomlar')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    photo_message_id = None
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as img_file:
                sent_photo_msg = await context.bot.send_photo(
                    chat_id=query.from_user.id,
                    photo=img_file
                )
                photo_message_id = sent_photo_msg.message_id
        except Exception as e:
            logger.error(f"Rasm yuborishda xatolik: {e}")
            await context.bot.send_message(chat_id=query.from_user.id, text="Rasm yuborishda xatolik yuz berdi.")
    else:
        logger.warning(f"Rasm topilmadi: {image_path}")
    text_message_id = None
    if len(text_data) > 3500:
        await send_long_text_in_chunks(text_data, query.from_user.id, context)
        msg = await context.bot.send_message(chat_id=query.from_user.id, text="...", reply_markup=reply_markup)
        text_message_id = msg.message_id
    else:
        msg = await context.bot.send_message(chat_id=query.from_user.id, text=text_data, reply_markup=reply_markup)
        text_message_id = msg.message_id
    context.user_data['recipe_photo_msg_id'] = photo_message_id
    context.user_data['recipe_text_msg_id'] = text_message_id

async def back_to_taomlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    update_user_last_activity(user_id)
    query = update.callback_query
    await query.answer()
    photo_msg_id = context.user_data.get('recipe_photo_msg_id')
    if photo_msg_id:
        try:
            await context.bot.delete_message(chat_id=query.from_user.id, message_id=photo_msg_id)
        except Exception as e:
            logger.error(f"Rasm xabarni o'chirishda xatolik: {e}")
        context.user_data.pop('recipe_photo_msg_id', None)
    text_msg_id = context.user_data.get('recipe_text_msg_id')
    if text_msg_id:
        try:
            await context.bot.delete_message(chat_id=query.from_user.id, message_id=text_msg_id)
        except Exception as e:
            logger.error(f"Matn xabarni o'chirishda xatolik: {e}")
        context.user_data.pop('recipe_text_msg_id', None)
    await show_main_taomlar_menu(update, context)


# ============== ADMIN KOMANDALARI ==============
async def user_count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("Ushbu buyruq faqat admin uchun.")
        return

    # Bazadan userlarni olamiz
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id, last_activity FROM users")
                all_users = cur.fetchall()
    finally:
        conn.close()

    active_count = 0
    now = datetime.now()
    fail_count = 0
    for row in all_users:
        uid = row[0]
        last_active_dt = row[1]
        if not last_active_dt:
            continue
        if (now - last_active_dt) > timedelta(days=30):
            continue
        try:
            member = await context.bot.get_chat_member(uid, uid)
            if member.status in ("member", "administrator", "creator"):
                active_count += 1
        except Exception as e:
            logger.error(f"get_chat_member failed for {uid}: {e}")
            fail_count += 1

    msg_text = (
        f"Faol foydalanuvchilar (so'nggi 30 kunda): {active_count}\n"
        f"(Tekshirib bo'lmaganlar: {fail_count} ta — odatda botni bloklagan yoki mavjud emaslar.)"
    )
    await update.message.reply_text(msg_text)

# ============== ADMIN BROADCAST KOMANDASI ==============
async def admin_broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /admin_broadcast ni reply tarzida xabar yoki media ustida ishlatish.
    """
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("Ushbu buyruq faqat admin uchun.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Iltimos, reply tarzida xabar yoki media ustiga /admin_broadcast yuboring.")
        return

    # Yangi broadcast yaratib, id ni olamiz
    broadcast_id = create_broadcast(admin_id=user_id)

    # endi bazadagi barcha foydalanuvchilarni ro'yxatga olish
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM users")
                all_users = cur.fetchall()
    finally:
        conn.close()

    broadcast_count = 0
    fail_count = 0

    for row in all_users:
        uid = row[0]
        # Avval so'nggi main menu xabarini o'chirishga harakat qilamiz
        last_main_menu_id = get_user_last_main_menu(uid)
        if last_main_menu_id:
            try:
                await context.bot.delete_message(chat_id=uid, message_id=last_main_menu_id)
                delete_user_last_main_menu(uid)
            except Exception as e:
                logger.error(f"User {uid}: Oldingi main menu xabari o'chirishda xatolik: {e}")

        # forward/copy message
        try:
            sent_msg = await context.bot.copy_message(
                chat_id=uid,
                from_chat_id=update.effective_chat.id,
                message_id=update.message.reply_to_message.message_id
            )
            broadcast_count += 1
            add_broadcast_message(broadcast_id, uid, sent_msg.message_id)

            # Yangi asosiy menyu
            main_menu_text = "Quyidagilardan birini tanlang:"
            main_menu_keyboard = [
                [InlineKeyboardButton("Taomlar 🍽", callback_data='main_taomlar')],
                [InlineKeyboardButton("Mashg'ulotlar 🏋️", callback_data='main_mashgulotlar')],
                [InlineKeyboardButton("Davolanish 🏥", callback_data='main_davolanish')]
            ]
            sent_main_menu = await context.bot.send_message(chat_id=uid, text=main_menu_text, reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
            set_user_last_main_menu(uid, sent_main_menu.message_id)

        except Exception as e:
            logger.error(f"Broadcast to {uid} failed: {e}")
            fail_count += 1

    await update.message.reply_text(
        f"Xabar forward qilindi. Muvaffaqiyatli: {broadcast_count} ta. Xato: {fail_count} ta.\n"
        f"Broadcast ID = {broadcast_id}"
    )

async def admin_edit_broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /edit_broadcast <broadcast_id> <yangi matn>
    """
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("Ushbu buyruq faqat admin uchun.")
        return

    args = update.message.text.split(maxsplit=2)
    if len(args) < 3:
        await update.message.reply_text("Iltimos, /edit_broadcast <broadcast_id> <yangi matn> formatida yuboring.")
        return

    try:
        broadcast_id = int(args[1])
    except ValueError:
        await update.message.reply_text("broadcast_id noto‘g‘ri.")
        return

    new_text = args[2]

    # endi DBdan o‘sha broadcast qaydlarini topib edit qilamiz
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT broadcast_id FROM broadcasts WHERE broadcast_id=%s", (broadcast_id,))
                row = cur.fetchone()
                if not row:
                    await update.message.reply_text("Bunday broadcast_id topilmadi.")
                    return
    finally:
        conn.close()

    edit_count, fail_count = edit_broadcast_messages(broadcast_id, new_text, context)
    await update.message.reply_text(
        f"Broadcast {broadcast_id} tahrirlandi.\n"
        f"Muvaffaqiyatli: {edit_count}, xato: {fail_count}."
    )

async def admin_delete_broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /delete_broadcast <broadcast_id>
    """
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("Ushbu buyruq faqat admin uchun.")
        return

    args = update.message.text.split(maxsplit=1)
    if len(args) < 2:
        await update.message.reply_text("Iltimos, /delete_broadcast <broadcast_id> formatida yuboring.")
        return

    try:
        broadcast_id = int(args[1])
    except ValueError:
        await update.message.reply_text("broadcast_id noto‘g‘ri.")
        return

    # Bazadan o'chiramiz
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT broadcast_id FROM broadcasts WHERE broadcast_id=%s", (broadcast_id,))
                row = cur.fetchone()
                if not row:
                    await update.message.reply_text("Bunday broadcast_id topilmadi.")
                    return
    finally:
        conn.close()

    # Endi broadcast va message-larini o'chirish
    # (ON DELETE CASCADE bo'lgani uchun broadcasts dan o'chsa, broadcast_messages ham o'chadi)
    # ammo telegramda o'z xabarlarini ham delete qilish:
    rows = get_broadcast_messages(broadcast_id)
    delete_count = 0
    fail_count = 0
    for (chat_id, msg_id) in rows:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            delete_count += 1
        except Exception as e:
            logger.error(f"Delete failed for chat {chat_id}, msg {msg_id}: {e}")
            fail_count += 1

    delete_broadcast(broadcast_id)

    await update.message.reply_text(
        f"Broadcast {broadcast_id} o'chirildi.\n"
        f"Muvaffaqiyatli: {delete_count}, xato: {fail_count}."
    )


# ============== ASOSIY MENU CALLBACK: Taomlar / Mashg'ulotlar / Davolanish ==============
async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    update_user_last_activity(user_id)

    await query.answer()
    choice = query.data.split('_')[1]
    if choice == 'taomlar':
        await show_main_taomlar_menu(update, context)
    elif choice == 'mashgulotlar':
        text = "Mashg'ulotlar bo'limi. Tanlang:"
        keyboard = [
            [InlineKeyboardButton("Erkak", callback_data='mash_erkak')],
            [InlineKeyboardButton("Ayol", callback_data='mash_ayol')],
            [InlineKeyboardButton("Ortga⬅️", callback_data='main_menu_back')]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))
    elif choice == 'davolanish':
        await show_davolanish_categories(update, context)

async def postcalc_back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    update_user_last_activity(user_id)
    await query.answer()

    main_menu_text = "Quyidagilardan birini tanlang:"
    main_menu_keyboard = [
        [InlineKeyboardButton("Taomlar 🍽", callback_data='main_taomlar')],
        [InlineKeyboardButton("Mashg'ulotlar 🏋️", callback_data='main_mashgulotlar')],
        [InlineKeyboardButton("Davolanish 🏥", callback_data='main_davolanish')]
    ]
    await query.edit_message_text(text=main_menu_text, reply_markup=InlineKeyboardMarkup(main_menu_keyboard))

# ============== Mashg'ulotlar bo'limi (Erkak/Ayol) ==============
async def mash_gender_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    gender = query.data.split('_')[1]  # erkak | ayol

    if gender == 'erkak':
        text = "Erkaklar uchun mashg'ulot bo'limi. Tanlang:"
        keyboard = [
            [InlineKeyboardButton("Vazn olish", callback_data='mash_erkak_gain')],
            [InlineKeyboardButton("Vazn saqlash", callback_data='mash_erkak_maintain')],
            [InlineKeyboardButton("Vazn yo'qotish", callback_data='mash_erkak_lose')],
            [InlineKeyboardButton("Ortga⬅️", callback_data='mash_erkak_back')]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        text = "Ayollar uchun mashg'ulot bo'limi. Tanlang:"
        keyboard = [
            [InlineKeyboardButton("Vazn olish", callback_data='mash_ayol_gain')],
            [InlineKeyboardButton("Vazn saqlash", callback_data='mash_ayol_maintain')],
            [InlineKeyboardButton("Vazn yo'qotish", callback_data='mash_ayol_lose')],
            [InlineKeyboardButton("Ortga⬅️", callback_data='mash_ayol_back')]
        ]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def mash_ortga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Mashg'ulotlar bo'limidan Ortga bosilganda.
    """
    query = update.callback_query
    await query.answer()

    text = "Mashg'ulotlar bo'limi. Tanlang:"
    keyboard = [
        [InlineKeyboardButton("Erkak", callback_data='mash_erkak')],
        [InlineKeyboardButton("Ayol", callback_data='mash_ayol')],
        [InlineKeyboardButton("Ortga⬅️", callback_data='main_menu_back')]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def main_menu_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asosiy menyuga qaytish (Mashg'ulotlar bo'limidan).
    """
    query = update.callback_query
    await query.answer()

    main_menu_text = "Quyidagilardan birini tanlang:"
    main_menu_keyboard = [
        [InlineKeyboardButton("Taomlar 🍽", callback_data='main_taomlar')],
        [InlineKeyboardButton("Mashg'ulotlar 🏋️", callback_data='main_mashgulotlar')],
        [InlineKeyboardButton("Davolanish 🏥", callback_data='main_davolanish')]
    ]

    await query.edit_message_text(
        text=main_menu_text,
        reply_markup=InlineKeyboardMarkup(main_menu_keyboard)
    )

# ============== Mashg'ulotlar (erkak) ==============
async def mash_erkak_gain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "Erkaklar uchun Vazn olish mashqlari:\n\n"
            "1)Push-up (erga suyanib ko'tarilish):\n"
            "   -Qanday bajariladi: Kaftlaringizni yerdan yelkangiz kengligida qo'yib, tanangizni to'g'ri tutgan holda, tirsaklaringizni bukib, yuqoriga va pastga harakatlaning.\n"
            "   -Foydalari: Ko'krak, tritseps va yelka mushaklarini kuchaytiradi.\n"
            "   -Qancha vaqtda bajariladi: Haftasiga 4-5 kun, har kuni 3 ta setda 10-15 marta.\n"
            "   -Energiya sarfi: 1 daqiqada taxminan 7-10 kkal.\n"
            "   -Kimlarga mumkin emas: Yurak yoki qo'l bo'g'imlari bilan bog'liq muammolar bo'lganlarga ehtiyot bo'lish kerak.\n\n"
            "2)Dumbbell bilan skamyadan turib ko'tarish (agar dumbbell bo'lmasa, suv bilan to'ldirilgan shisha idish ishlatish mumkin):\n"
            "   -Qanday bajariladi: Har ikki qo'lga og'irlik olib, tirsakni bukib, yuqoriga ko'taring va asta-sekin pastga tushiring.\n"
            "   -Foydalari: Qo'l va yelka mushaklarini rivojlantiradi.\n"
            "   -Qancha vaqtda bajariladi: Haftasiga 3-4 kun, 3 ta setda 12-15 marta.\n"
            "   -Energiya sarfi: 10 daqiqada taxminan 30-40 kkal.\n\n"
            "Mashqlar bo'yicha umumiy tavsiyalar:\n"
            "-Mashqlarni har doim qizish bilan boshlang (5-10 daqiqa).\n"
            "-Har bir mashqni bajarishda to'g'ri holatda turing, noto'g'ri texnika jarohatlarga olib kelishi mumkin.\n"
            "-Mashqlardan keyin cho'zish mashqlarini bajaring (2-3 daqiqa).\n"
            "-Mashqlarni bajarishda ortiqcha kuchanishdan saqlaning. Agar o'zingizni noqulay his qilsangiz, darhol to'xtang.\n"
            "-Suv ichishni unutmang: mashqdan oldin, davomida va keyin.\n"
            "👉 @hayot_balansi 👈\n"

    )
    keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data='mash_erkak_back')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def mash_erkak_maintain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "Erkaklar uchun Vazn saqlash mashqlari:\n"
        "Mashqlar ro'yxati:\n"
        "1)Plank (tanani to'g'ri ushlab turish):\n"

        "-Qanday bajariladi: Yerni tirsaklar va barmoqlar bilan ushlab, tanani to'g'ri chiziqda ushlang.\n"
        "-Foydalari: Qorin mushaklarini kuchaytiradi va umurtqa tayanchini mustahkamlaydi.\n"
        "-Qancha vaqtda bajariladi: Haftasiga 3-5 kun, har bir mashqni 3-4 daqiqadan.\n"
        "-Energiya sarfi: 5 daqiqada 15-20 kkal.\n"
        "-Kimlarga mumkin emas: Bel yoki qo'l og'rig'i bo'lganlarga ehtiyot bo'lish kerak.\n\n"
        "2)Step-up (zina yoki skamya ustiga chiqib tushish):\n"

        "-Qanday bajariladi: Bir oyog'ingiz bilan zinaga yoki skamyaga chiqib, boshqa oyog'ingizni torting, keyin asta-sekin pastga tushing.\n"
        "-Foydalari: Oyoq mushaklarini rivojlantiradi, yurak-qon tomir faoliyatini yaxshilaydi.\n"
        "-Qancha vaqtda bajariladi: Haftasiga 3-4 kun, har bir mashqni 10-15 daqiqadan.\n"
        "-Energiya sarfi: 10 daqiqada 70-100 kkal.\n\n"
        "Mashqlar bo'yicha umumiy tavsiyalar:\n"
        "-Mashqlarni har doim qizish bilan boshlang (5-10 daqiqa).\n"
        "-Har bir mashqni bajarishda to'g'ri holatda turing, noto'g'ri texnika jarohatlarga olib kelishi mumkin.\n"
        "-Mashqlardan keyin cho'zish mashqlarini bajaring (2-3 daqiqa).\n"
        "-Mashqlarni bajarishda ortiqcha kuchanishdan saqlaning. Agar o'zingizni noqulay his qilsangiz, darhol to'xtang.\n"
        "-Suv ichishni unutmang: mashqdan oldin, davomida va keyin.\n"
        "👉 @hayot_balansi 👈\n"

    )
    keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data='mash_erkak_back')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def mash_erkak_lose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "Erkaklar uchun Vazn yo'qotish mashqlari:\n"
        "Mashqlar ro'yxati:\n"
        "1)Jumping Jacks (o'rnidan sakrash):\n"

        "-Qanday bajariladi: Oyoq va qo'llarni yon tomonlarga ochib, sakrab tushish va qo'llarni pastga tushirish.\n"
        "-Foydalari: Kardio faoliyatni yaxshilaydi va yog'larni yo'qotishga yordam beradi.\n"
        "-Qancha vaqtda bajariladi: Haftasiga 4-5 kun, har kuni 3 ta setda 2-3 daqiqadan.\n"
        "-Energiya sarfi: 10 daqiqada 80-100 kkal.\n"
        "-Kimlarga mumkin emas: Yurak muammolari yoki yuqori qon bosimi bo'lganlarga ehtiyot bo'lish kerak.\n\n"
        "2)Burpee (tezkor mashq turi):\n"

        "-Qanday bajariladi: Turgan holatda boshlang, tiz cho'kib, yerga yoting, tezlik bilan qayta turing va sakrang.\n"
        "-Foydalari: Butun tana mushaklarini faollashtiradi, yog'larni yoqadi.\n"
        "-Qancha vaqtda bajariladi: Haftasiga 3-4 kun, 10 daqiqadan.\n"
        "-Energiya sarfi: 10 daqiqada 120-150 kkal.\n\n"
        "Mashqlar bo'yicha umumiy tavsiyalar:\n"
        "-Mashqlarni har doim qizish bilan boshlang (5-10 daqiqa).\n"
        "-Har bir mashqni bajarishda to'g'ri holatda turing, noto'g'ri texnika jarohatlarga olib kelishi mumkin.\n"
        "-Mashqlardan keyin cho'zish mashqlarini bajaring (2-3 daqiqa).\n"
        "-Mashqlarni bajarishda ortiqcha kuchanishdan saqlaning. Agar o'zingizni noqulay his qilsangiz, darhol to'xtang.\n"
        "-Suv ichishni unutmang: mashqdan oldin, davomida va keyin.\n"
        "👉 @hayot_balansi 👈\n"

    )
    keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data='mash_erkak_back')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def mash_erkak_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Mashg'ulotlar bo'limi. Tanlang:"
    keyboard = [
        [InlineKeyboardButton("Erkak", callback_data='mash_erkak')],
        [InlineKeyboardButton("Ayol", callback_data='mash_ayol')],
        [InlineKeyboardButton("Ortga⬅️", callback_data='main_menu_back')]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

# ============== Mashg'ulotlar (ayol) ==============
async def mash_ayol_gain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "Ayollar uchun Vazn olish mashqlari:\n"
        "Mashqlar ro'yxati:\n"
        "1)Squat (o'tqazish mashqi):\n"

        "-Qanday bajariladi: Oyoqlarni elkangiz kengligida qo'yib, qo'llarni oldinga cho'zib, asta-sekin tiz cho'kib o'tiring, keyin tiklaning.\n"
        "-Foydalari: Son va dumba mushaklarini rivojlantiradi.\n"
        "-Qancha vaqt bajariladi: Haftasiga 4-5 kun, 3 ta setda 12-15 marta.\n"
        "-Energiya sarfi: 10 daqiqada taxminan 40-50 kkal.\n"
        "-Kimlarga mumkin emas: Tizza og'rig'i yoki bo'g'im muammolari bo'lganlarga ehtiyot bo'lish kerak.\n\n"
        "2)Leg Raise (oyoqlarni ko'tarish):\n"

        "-Qanday bajariladi: Yotgan holda oyoqlarni to'g'ri chiziqda ko'taring va asta-sekin pastga tushiring.\n"
        "-Foydalari: Qorin mushaklarini mustahkamlaydi va dumba mushaklarini faollashtiradi.\n"
        "-Qancha vaqt bajariladi: Haftasiga 4-5 kun, 3 ta setda 10-15 marta.\n"
        "-Energiya sarfi: 10 daqiqada taxminan 30-40 kkal.\n\n"
        "Mashqlar bo'yicha umumiy tavsiyalar:\n"
        "-Qizish: Mashqlardan oldin 5-10 daqiqa davomida yengil cho'zish mashqlarini bajaring.\n"
        "-Nafas olish: Mashqlar davomida to'g'ri nafas oling. Mashq qiyinlashganda nafas oling, yengillashganda nafas chiqaring.\n"
        "-Suv ichish: Mashqdan oldin, davomida va keyin suv ichishni unutmang.\n"
        "-To'g'ri ovqatlanish: Maqsadingizga qarab kaloriya iste'molini kuzating. Vazn olish uchun ko'proq, vazn yo'qotish uchun kamroq kaloriya iste'mol qiling.\n"
        "-Dam olish: Haftasiga kamida bir kun tanaffus qiling.\n"
        "👉 @hayot_balansi 👈\n"

    )
    keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data='mash_ayol_back')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def mash_ayol_maintain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
         "Ayollar uchun Vazn saqlash mashqlari:\n"
            "Mashqlar ro'yxati:\n"
            "1)Plank (tanani to'g'ri ushlab turish):\n"

            "-Qanday bajariladi: Tirsaklarni yerga qo'yib, tanani to'g'ri ushlang.\n"
            "-Foydalari: Qorin mushaklarini mustahkamlaydi, umurtqa va tayanchni kuchaytiradi.\n"
            "-Qancha vaqt bajariladi: Haftasiga 3-5 kun, 3-4 ta setda 30 soniyadan.\n"
            "-Energiya sarfi: 10 daqiqada taxminan 30-40 kkal.\n"
            "-Kimlarga mumkin emas: Bel yoki yelka og'rig'i bo'lganlarga ehtiyot bo'lish kerak.\n\n"
            "2)Step-Up (zina yoki skamya ustiga chiqib tushish):\n"

            "-Qanday bajariladi: Bir oyog'ingiz bilan skamyaga chiqing, ikkinchi oyog'ingizni torting va asta-sekin pastga tushing.\n"
            "-Foydalari: Oyoq va dumba mushaklarini mustahkamlaydi.\n"
            "-Qancha vaqt bajariladi: Haftasiga 3-4 kun, har bir mashqni 15-20 daqiqadan.\n"
            "-Energiya sarfi: 10 daqiqada taxminan 60-80 kkal.\n\n"
            "Mashqlar bo'yicha umumiy tavsiyalar:\n"
            "-Qizish: Mashqlardan oldin 5-10 daqiqa davomida yengil cho'zish mashqlarini bajaring.\n"
            "-Nafas olish: Mashqlar davomida to'g'ri nafas oling. Mashq qiyinlashganda nafas oling, yengillashganda nafas chiqaring.\n"
            "-Suv ichish: Mashqdan oldin, davomida va keyin suv ichishni unutmang.\n"
            "-To'g'ri ovqatlanish: Maqsadingizga qarab kaloriya iste'molini kuzating. Vazn olish uchun ko'proq, vazn yo'qotish uchun kamroq kaloriya iste'mol qiling.\n"
            "-Dam olish: Haftasiga kamida bir kun tanaffus qiling.\n"
            "👉 @hayot_balansi 👈\n"

    )
    keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data='mash_ayol_back')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def mash_ayol_lose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
         "Ayollar uchun Vazn yo'qotish mashqlari:\n"
            "Mashqlar ro'yxati:\n"
            "1)Jumping Jacks (o'rnidan sakrash):\n"

            "-Qanday bajariladi: Qo'l va oyoqlarni yon tomonlarga ochib sakrab tushing, keyin pastga qayting.\n"
            "-Foydalari: Yurak-qon tomir faoliyatini yaxshilaydi, yog'larni yoqishga yordam beradi.\n"
            "-Qancha vaqt bajariladi: Haftasiga 4-5 kun, har kuni 3 ta setda 2-3 daqiqadan.\n"
            "-Energiya sarfi: 10 daqiqada taxminan 70-90 kkal.\n"
            "-Kimlarga mumkin emas: Yurak yoki yuqori qon bosimi muammolari bo'lganlarga ehtiyot bo'lish kerak.\n\n"
            "2)Mountain Climbers (tog'ga chiqish mashqi):\n"

            "-Qanday bajariladi: Plank holatida oyoqlarni navbatma-navbat ko'krakka torting.\n"
            "-Foydalari: Qorin va oyoq mushaklarini kuchaytiradi, yog'larni yoqadi.\n"
            "-Qancha vaqt bajariladi: Haftasiga 3-4 kun, 10 daqiqadan.\n"
            "-Energiya sarfi: 10 daqiqada taxminan 80-100 kkal.\n\n"

            "Mashqlar bo'yicha umumiy tavsiyalar:\n"
            "-Qizish: Mashqlardan oldin 5-10 daqiqa davomida yengil cho'zish mashqlarini bajaring.\n"
            "-Nafas olish: Mashqlar davomida to'g'ri nafas oling. Mashq qiyinlashganda nafas oling, yengillashganda nafas chiqaring.\n"
            "-Suv ichish: Mashqdan oldin, davomida va keyin suv ichishni unutmang.\n"
            "-To'g'ri ovqatlanish: Maqsadingizga qarab kaloriya iste'molini kuzating. Vazn olish uchun ko'proq, vazn yo'qotish uchun kamroq kaloriya iste'mol qiling.\n"
            "-Dam olish: Haftasiga kamida bir kun tanaffus qiling.\n"
            "👉 @hayot_balansi 👈\n"


    )
    keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data='mash_ayol_back')]]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

async def mash_ayol_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Mashg'ulotlar bo'limi. Tanlang:"
    keyboard = [
        [InlineKeyboardButton("Erkak", callback_data='mash_erkak')],
        [InlineKeyboardButton("Ayol", callback_data='mash_ayol')],
        [InlineKeyboardButton("Ortga⬅️", callback_data='main_menu_back')]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

# ============== DAVOLANISH BO'LIMI (YANGI FUNKTSIONAL) ==============
# Top-level: 11 ta kategoriya tugmalari

async def show_davolanish_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Davolanish bo'limi. Quyidagi kasallik kategoriyalaridan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("1. Yurak-qon tomir kasalliklari", callback_data="dav_cat_yurak")],
        [InlineKeyboardButton("2. Oshqozon-ichak kasalliklari", callback_data="dav_cat_oshqozon")],
        [InlineKeyboardButton("3. Immunitet va shamollashga bog'liq kasalliklar", callback_data="dav_cat_immunitet")],
        [InlineKeyboardButton("4. Buyrak va siydik yo'llari kasalliklari", callback_data="dav_cat_buyrak")],
        [InlineKeyboardButton("5. Nafas olish tizimi kasalliklari", callback_data="dav_cat_nafas")],
        [InlineKeyboardButton("6. Jigar va qand kasalliklari", callback_data="dav_cat_jigar")],
        [InlineKeyboardButton("7. Asab va ruhiy muammolar", callback_data="dav_cat_asab")],
        [InlineKeyboardButton("8. Erkaklar va ayollar salomatligi", callback_data="dav_cat_salomatlik")],
        [InlineKeyboardButton("9. Bo'g'im, suyak va umurtqa muammolari", callback_data="dav_cat_bogim")],
        [InlineKeyboardButton("10. Teri va kosmetologik muammolar", callback_data="dav_cat_teri")],
        [InlineKeyboardButton("11. Og'iz va tish kasalliklari", callback_data="dav_cat_tish")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="dav_ortga")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

# Kategoriya tanlash: dav_cat_*
async def dav_category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    if data == "dav_cat_yurak":
        await show_yurak_menu(update, context)
    elif data == "dav_cat_oshqozon":
        await show_oshqozon_menu(update, context)
    elif data == "dav_cat_immunitet":
        await show_immunitet_menu(update, context)
    elif data == "dav_cat_buyrak":
        await show_buyrak_menu(update, context)
    elif data == "dav_cat_nafas":
        await show_nafas_menu(update, context)
    elif data == "dav_cat_jigar":
        await show_jigar_menu(update, context)
    elif data == "dav_cat_asab":
        await show_asab_menu(update, context)
    elif data == "dav_cat_salomatlik":
        await show_salomatlik_menu(update, context)
    elif data == "dav_cat_bogim":
        await show_bogim_menu(update, context)
    elif data == "dav_cat_teri":
        await show_teri_menu(update, context)
    elif data == "dav_cat_tish":
        await show_tish_menu(update, context)
    else:
        await query.answer("Noma'lum kategoriya!")

# Har bir kategoriya uchun sub-menu funksiyalari

async def show_yurak_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Yurak-qon tomir kasalliklari bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Qon bosimi baland bo'lsa", callback_data="dav_yurak_qon_baland")],
        [InlineKeyboardButton("Gipertoniyada", callback_data="dav_yurak_gipertoniyada")],
        [InlineKeyboardButton("Qon bosimi pasayganda (Gipotoniya)", callback_data="dav_yurak_gipotoniya")],
        [InlineKeyboardButton("Yurak siqilishdanomli", callback_data="dav_yurak_siqilish")],
        [InlineKeyboardButton("Yurak xastaligida", callback_data="dav_yurak_xastalik")],
        [InlineKeyboardButton("Miokard infarktidanomli", callback_data="dav_yurak_infarkt")],
        [InlineKeyboardButton("Qon tomir devorlarini mustahkamlashda", callback_data="dav_yurak_devorlar")],
        [InlineKeyboardButton("Qon yurgizishda", callback_data="dav_yurak_yurgizish")],
        [InlineKeyboardButton("Yurak qon tomirlarini tozalashda", callback_data="dav_yurak_tozalash")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_oshqozon_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Oshqozon-ichak kasalliklari bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Gastritda", callback_data="dav_oshqozon_gastrit")],
        [InlineKeyboardButton("Oshqozon yarasi", callback_data="dav_oshqozon_yarasi")],
        [InlineKeyboardButton("Ich ketganda", callback_data="dav_oshqozon_ichketganda")],
        [InlineKeyboardButton("Ichak kasalliklarida", callback_data="dav_oshqozon_ichak")],
        [InlineKeyboardButton("Qabziyatda (Ich qotishi)", callback_data="dav_oshqozon_qabziyat")],
        [InlineKeyboardButton("Qorin dam bo'lsa", callback_data="dav_oshqozon_qorin")],
        [InlineKeyboardButton("Moddalar almashinuvini yaxshilashda", callback_data="dav_oshqozon_almashinuv")],
        [InlineKeyboardButton("O'n ikki barmoqli ichak yarasida", callback_data="dav_oshqozon_ondb")],
        [InlineKeyboardButton("Oshqozon og'ri, zaharlanganda", callback_data="dav_oshqozon_zaharlangan")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_immunitet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Immunitet va shamollashga bog'liq kasalliklar bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Immunitetni kuchaytirishda", callback_data="dav_immunitet_kuchaytirish")],
        [InlineKeyboardButton("Shamollashda", callback_data="dav_immunitet_shamollash")],
        [InlineKeyboardButton("Angina va shamollashda", callback_data="dav_immunitet_angina")],
        [InlineKeyboardButton("Gripp, tumov va shamollashda", callback_data="dav_immunitet_gripp")],
        [InlineKeyboardButton("Yuqori nafas yo'llari yallig'langanda", callback_data="dav_immunitet_yuqori")],
        [InlineKeyboardButton("Isitmalaganda", callback_data="dav_immunitet_isitmala")],
        [InlineKeyboardButton("Faringitda", callback_data="dav_immunitet_faringit")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_buyrak_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Buyrak va siydik yo'llari kasalliklari bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Buyrak dardida", callback_data="dav_buyrak_dardi")],
        [InlineKeyboardButton("Buyrakda qum-tosh bo'lsa", callback_data="dav_buyrak_qumtosh")],
        [InlineKeyboardButton("Piyelonefrit va surunkali tsistitda", callback_data="dav_buyrak_piyelonefrit")],
        [InlineKeyboardButton("Siydik chiqarish yo'llarida mikrob bo'lganda", callback_data="dav_buyrak_mikrob")],
        [InlineKeyboardButton("Siydik tuta olmaslikda", callback_data="dav_buyrak_tutaolmaslik")],
        [InlineKeyboardButton("Peshob yo'llari achishishida", callback_data="dav_buyrak_peshob")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_nafas_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Nafas olish tizimi kasalliklari bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Bronxitda", callback_data="dav_nafas_bronxit")],
        [InlineKeyboardButton("Bronxial astmada", callback_data="dav_nafas_astma")],
        [InlineKeyboardButton("O'pka silida (Sil kasalligi)", callback_data="dav_nafas_opka")],
        [InlineKeyboardButton("Nafas qisilganda", callback_data="dav_nafas_qisilgan")],
        [InlineKeyboardButton("Tumovda", callback_data="dav_nafas_tumov")],
        [InlineKeyboardButton("Zotiljamda (Pnevmoniya)", callback_data="dav_nafas_zotiljam")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_jigar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Jigar va qand kasalliklari bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Jigar og'rig'ida va jigar qurti", callback_data="dav_jigar_ogrigida")],
        [InlineKeyboardButton("Jigar xastaligida", callback_data="dav_jigar_xastalik")],
        [InlineKeyboardButton("Jigar faoliyatini yaxshilashda", callback_data="dav_jigar_faoliyat")],
        [InlineKeyboardButton("Gepatit (sariq kasalligi)", callback_data="dav_jigar_gepatit")],
        [InlineKeyboardButton("Qand kasalida", callback_data="dav_jigar_qand")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_asab_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Asab va ruhiy muammolar bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Asabiylashganda", callback_data="dav_asab_asabiylash")],
        [InlineKeyboardButton("Kayfiyatni ko'tarishda", callback_data="dav_asab_kayfiyat")],
        [InlineKeyboardButton("Uyqusizlikda", callback_data="dav_asab_uyqusizlik")],
        [InlineKeyboardButton("Xotira susayganda", callback_data="dav_asab_xotira")],
        [InlineKeyboardButton("Ruhiyatni saqlashda", callback_data="dav_asab_ruhiyat")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_salomatlik_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Erkaklar va ayollar salomatligi bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Jinsiy quvvatni oshirishda", callback_data="dav_salomatlik_jinsi")],
        [InlineKeyboardButton("Shahvatni kuchaytirishda", callback_data="dav_salomatlik_shahvat")],
        [InlineKeyboardButton("Homilador va emizikli onalar uchun", callback_data="dav_salomatlik_homilador")],
        [InlineKeyboardButton("Xayz ko'p kelganda", callback_data="dav_salomatlik_xayz")],
        [InlineKeyboardButton("Qin shamollashi – eroziyada", callback_data="dav_salomatlik_qin")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_bogim_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Bo'g'im, suyak va umurtqa muammolari bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Revmatizmda", callback_data="dav_bogim_revmatizm")],
        [InlineKeyboardButton("Artritda", callback_data="dav_bogim_artrit")],
        [InlineKeyboardButton("Bo'g'imlar og'riganda", callback_data="dav_bogim_ogriganda")],
        [InlineKeyboardButton("Umurtqa og'riganda", callback_data="dav_bogim_umurtqa")],
        [InlineKeyboardButton("Tizza og'riganda", callback_data="dav_bogim_tizza")],
        [InlineKeyboardButton("Bel og'rig'ida", callback_data="dav_bogim_bel")],
        [InlineKeyboardButton("Suyaklar og'riganda", callback_data="dav_bogim_suyak")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_teri_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Teri va kosmetologik muammolar bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Zamburug' kasalligida", callback_data="dav_teri_zamburug")],
        [InlineKeyboardButton("Teri kuyganda", callback_data="dav_teri_kuygan")],
        [InlineKeyboardButton("Teri kasalliklarida", callback_data="dav_teri_kasallik")],
        [InlineKeyboardButton("Soch to'kilganda", callback_data="dav_teri_sochtokilganda")],
        [InlineKeyboardButton("Husnbuzarlarda", callback_data="dav_teri_husnbuzar")],
        [InlineKeyboardButton("Soch o'stirishda", callback_data="dav_teri_sochos")],
        [InlineKeyboardButton("Soch parvarishida", callback_data="dav_teri_sochparvarish")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

async def show_tish_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = "Og'iz va tish kasalliklari bo'limi. Quyidagi kasalliklardan birini tanlang:"
    keyboard = [
        [InlineKeyboardButton("Tish og'rig'ida", callback_data="dav_tish_ogrigida")],
        [InlineKeyboardButton("Tish kasalliklarida", callback_data="dav_tish_kasallik")],
        [InlineKeyboardButton("Stomatitda", callback_data="dav_tish_stomatit")],
        [InlineKeyboardButton("Og'izdagi nohush hid", callback_data="dav_tish_nohush")],
        [InlineKeyboardButton("Milkdan qon oqishida", callback_data="dav_tish_milk")],
        [InlineKeyboardButton("Ortga⬅️", callback_data="back_to_davolanish_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)

# Generic handler: tanlangan kasallik (subkategoriya) bo‘yicha matnni chiqarish
async def show_disease_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data_key = query.data  # masalan "dav_yurak_qon_baland"
    parts = data_key.split('_')
    if len(parts) < 3:
        await query.edit_message_text("Noto'g'ri ma'lumot.")
        return
    category = parts[1]
    disease_info = diseases_data.get(data_key)
    if disease_info is None:
        text = "Bu kasallik bo'yicha ma'lumot topilmadi."
    else:
        text = disease_info.get("text", "Ma'lumot mavjud emas.")
    # Belgilangan kategoriya bo‘yicha "Ortga" tugmasi
    back_callback = ""
    if category == "yurak":
        back_callback = "back_to_yurak_menu"
    elif category == "oshqozon":
        back_callback = "back_to_oshqozon_menu"
    elif category == "immunitet":
        back_callback = "back_to_immunitet_menu"
    elif category == "buyrak":
        back_callback = "back_to_buyrak_menu"
    elif category == "nafas":
        back_callback = "back_to_nafas_menu"
    elif category == "jigar":
        back_callback = "back_to_jigar_menu"
    elif category == "asab":
        back_callback = "back_to_asab_menu"
    elif category == "salomatlik":
        back_callback = "back_to_salomatlik_menu"
    elif category == "bogim":
        back_callback = "back_to_bogim_menu"
    elif category == "teri":
        back_callback = "back_to_teri_menu"
    elif category == "tish":
        back_callback = "back_to_tish_menu"
    else:
        back_callback = "back_to_davolanish_categories"
    keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data=back_callback)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if len(text) > 3500:
        await send_long_text_in_chunks(text, query.from_user.id, context)
        await context.bot.send_message(chat_id=query.from_user.id, text="...", reply_markup=reply_markup)
    else:
        await query.edit_message_text(text=text, reply_markup=reply_markup)

# Back tugmalari uchun handlerlar:
async def back_to_davolanish_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_davolanish_categories(update, context)

async def back_to_yurak_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_yurak_menu(update, context)

async def back_to_oshqozon_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_oshqozon_menu(update, context)

async def back_to_immunitet_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_immunitet_menu(update, context)

async def back_to_buyrak_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_buyrak_menu(update, context)

async def back_to_nafas_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_nafas_menu(update, context)

async def back_to_jigar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_jigar_menu(update, context)

async def back_to_asab_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_asab_menu(update, context)

async def back_to_salomatlik_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_salomatlik_menu(update, context)

async def back_to_bogim_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_bogim_menu(update, context)

async def back_to_teri_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_teri_menu(update, context)

async def back_to_tish_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_tish_menu(update, context)

async def dav_ortga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Davolanish bo'limidan Asosiy menuga qaytish.
    """
    query = update.callback_query
    await query.answer()

    main_menu_text = "Quyidagilardan birini tanlang:"
    main_menu_keyboard = [
        [InlineKeyboardButton("Taomlar 🍽", callback_data='main_taomlar')],
        [InlineKeyboardButton("Mashg'ulotlar 🏋️", callback_data='main_mashgulotlar')],
        [InlineKeyboardButton("Davolanish 🏥", callback_data='main_davolanish')]
    ]

    await query.edit_message_text(
        main_menu_text,
        reply_markup=InlineKeyboardMarkup(main_menu_keyboard)
    )

# ============== BOTGA HANDLERLARNI QO‘SHISH ==============
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # /start
    application.add_handler(CommandHandler("start", start))

    # Foydalanuvchi matn (age,height,weight)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_data))

    # Kunlik eslatma tugmalari
    application.add_handler(CallbackQueryHandler(daily_reminder_answer, pattern='^daily_(yes|no)$'))
    application.add_handler(CallbackQueryHandler(recipes_button_handler, pattern='^recipes$'))

    # Taomlar bo'limi
    application.add_handler(CallbackQueryHandler(show_main_taomlar_menu, pattern='^main_taomlar$'))
    application.add_handler(CallbackQueryHandler(show_dish_categories, pattern='^cat_'))
    application.add_handler(CallbackQueryHandler(show_recipe_callback, pattern='^(dish_|drink_|tort_|non_).*'))
    application.add_handler(CallbackQueryHandler(back_to_taomlar, pattern='^back_to_taomlar$'))
    application.add_handler(CallbackQueryHandler(postcalc_back_to_main, pattern='^postcalc_back_to_main$'))

    # Mashg'ulotlar
    application.add_handler(CallbackQueryHandler(main_menu_handler, pattern='^main_(mashgulotlar|davolanish)$'))
    application.add_handler(CallbackQueryHandler(mash_gender_handler, pattern='^mash_(erkak|ayol)$'))
    application.add_handler(CallbackQueryHandler(mash_erkak_gain, pattern='^mash_erkak_gain$'))
    application.add_handler(CallbackQueryHandler(mash_erkak_maintain, pattern='^mash_erkak_maintain$'))
    application.add_handler(CallbackQueryHandler(mash_erkak_lose, pattern='^mash_erkak_lose$'))
    application.add_handler(CallbackQueryHandler(mash_erkak_back, pattern='^mash_erkak_back$'))
    application.add_handler(CallbackQueryHandler(mash_ayol_gain, pattern='^mash_ayol_gain$'))
    application.add_handler(CallbackQueryHandler(mash_ayol_maintain, pattern='^mash_ayol_maintain$'))
    application.add_handler(CallbackQueryHandler(mash_ayol_lose, pattern='^mash_ayol_lose$'))
    application.add_handler(CallbackQueryHandler(mash_ayol_back, pattern='^mash_ayol_back$'))
    application.add_handler(CallbackQueryHandler(mash_ortga, pattern='^mash_ortga$'))
    application.add_handler(CallbackQueryHandler(main_menu_back, pattern='^main_menu_back$'))

    # Davolanish
    # Endi yangi davolanish bo‘limi: avval 11 ta kategoriya menyusi
    application.add_handler(CallbackQueryHandler(show_davolanish_categories, pattern='^main_davolanish$'))
    application.add_handler(CallbackQueryHandler(dav_category_handler, pattern='^dav_cat_'))
    # Kasalliklarni tanlash uchun: callback_data "dav_yurak_...", "dav_oshqozon_...", "dav_immunitet_...", "dav_buyrak_...", "dav_nafas_...", "dav_jigar_...", "dav_asab_...", "dav_salomatlik_...", "dav_bogim_...", "dav_teri_...", "dav_tish_..."
    application.add_handler(CallbackQueryHandler(show_disease_detail, pattern=r'^dav_(yurak|oshqozon|immunitet|buyrak|nafas|jigar|asab|salomatlik|bogim|teri|tish)_'))
    # Back tugmalari handlerlari
    application.add_handler(CallbackQueryHandler(back_to_davolanish_categories, pattern='^back_to_davolanish_categories$'))
    application.add_handler(CallbackQueryHandler(back_to_yurak_menu, pattern='^back_to_yurak_menu$'))
    application.add_handler(CallbackQueryHandler(back_to_oshqozon_menu, pattern='^back_to_oshqozon_menu$'))
    application.add_handler(CallbackQueryHandler(back_to_immunitet_menu, pattern='^back_to_immunitet_menu$'))
    application.add_handler(CallbackQueryHandler(back_to_buyrak_menu, pattern='^back_to_buyrak_menu$'))
    application.add_handler(CallbackQueryHandler(back_to_nafas_menu, pattern='^back_to_nafas_menu$'))
    application.add_handler(CallbackQueryHandler(back_to_jigar_menu, pattern='^back_to_jigar_menu$'))
    application.add_handler(CallbackQueryHandler(back_to_asab_menu, pattern='^back_to_asab_menu$'))
    application.add_handler(CallbackQueryHandler(back_to_salomatlik_menu, pattern='^back_to_salomatlik_menu$'))
    application.add_handler(CallbackQueryHandler(back_to_bogim_menu, pattern='^back_to_bogim_menu$'))
    application.add_handler(CallbackQueryHandler(back_to_teri_menu, pattern='^back_to_teri_menu$'))
    application.add_handler(CallbackQueryHandler(back_to_tish_menu, pattern='^back_to_tish_menu$'))
    application.add_handler(CallbackQueryHandler(dav_ortga, pattern='^dav_ortga$'))

    # /users, /admin_broadcast, /edit_broadcast, /delete_broadcast
    application.add_handler(CommandHandler("users", user_count_command))
    application.add_handler(CommandHandler("admin_broadcast", admin_broadcast_command))
    application.add_handler(CommandHandler("edit_broadcast", admin_edit_broadcast_command))
    application.add_handler(CommandHandler("delete_broadcast", admin_delete_broadcast_command))

    logger.info("Bot ishga tushirildi...")
    application.run_polling()

if __name__ == '__main__':
    main()
