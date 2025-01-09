
import os
import logging
import json
from datetime import datetime, timedelta
from images_paths import images_paths
from recipes_texts import recipes_texts
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery,
    InputMediaPhoto, InputMediaDocument
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ============== LOGGER (log) sozlamalari ==============
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============== ADMIN IDs: Siz bu yerga o‘z ID raqamingizni yozasiz ==============
ADMIN_IDS = [7465094605]  # <-- O'zingizning telegram ID raqamingizni kiriting (yoki ro'yxat shaklida bir nechtasini)

# ============== TOKEN (o'zingizning BOT_TOKEN ni kiriting) ==============
BOT_TOKEN = "8018294597:AAEqpbRN7RU78-99TNbxr1ZCWs8R_qdvgQk"

# ============== GLOBAL o'zgaruvchilar ==============
DATA_FILE = "data.json"  # foydalanuvchi ma’lumotlari saqlanadigan fayl



# ============== JSON orqali ma’lumotlarni saqlash/yuklash ==============
def load_data():
    """
    data.json fayldan foydalanuvchi ma'lumotlarini yuklab,
    lug'at ko'rinishida qaytaradi.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_data(data: dict):
    """
    Lug'at ko'rinishidagi ma'lumotlarni data.json ga yozib qo'yadi.
    """
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ============== Yordamchi funksiyalar (uzun matnni bo‘lib yuborish) ==============
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



# ============== START KOMANDASI ==============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Global data.json
    bot_data = context.bot_data.setdefault("users_db", load_data())

    str_id = str(chat_id)
    # Kimdir /start qilgan bo‘lsa, uni bazaga qo‘shib qo‘yamiz (agar hali bo‘lmasa)
    if str_id not in bot_data:
        bot_data[str_id] = {
            "lang": None,
            "age": None,
            "height": None,
            "weight": None,
            "last_activity": None,  # foydalanuvchi so‘nggi marta qachon keldi
        }
    # har safar /start bosilganda last_activity yangilanadi
    bot_data[str_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_data(bot_data)

    text = (
        "O'zbekcha:\n"
        "Assalomu alaykum!☺️ Sog'lom turmush tarzini targ'ib qiluvchi botga xush kelibsiz!\n"
        "Iltimos, o'zingizga qulay tilni tanlang.\n\n"

        "Русский:\n"
        "Ассаламу алайкум!☺️ Добро пожаловать в бота, продвигающего здоровый образ жизни!\n"
        "Пожалуйста, выберите удобный для вас язык.\n\n"

        "English:\n"
        "Assalamu alaykum!☺️ Welcome to the bot promoting a healthy lifestyle!\n"
        "Please select your preferred language."
    )

    keyboard = [
        [
            InlineKeyboardButton("O'zbekcha 🇺🇿", callback_data='lang_uz'),
            InlineKeyboardButton("Русский 🇷🇺", callback_data='lang_ru'),
            InlineKeyboardButton("English 🇺🇸", callback_data='lang_en')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


# ============== TIL TANLASH CALLBACK ==============
async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split('_')[1]  # masalan 'uz', 'ru', 'en'

    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(query.from_user.id)

    if str_id in bot_data:
        bot_data[str_id]["lang"] = lang
        # yangilangan sana
        bot_data[str_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(bot_data)

    messages = {
        'uz': "Til tanlandi: O'zbekcha. Keling, boshlaymiz!🤗\nYoshingiz, bo'yingiz (sm) va vazningizni (kg) kiriting (masalan: 25, 175, 70).",
        'ru': "Вы выбрали русский язык. Давайте начнём!🤗\nВведите ваш возраст, рост (см) и вес (кг) (например: 25, 175, 70).",
        'en': "You selected English. Let's start!🤗\nPlease enter your age, height (cm), and weight (kg) (e.g., 25, 175, 70)."
    }
    await query.edit_message_text(text=messages[lang])


# ============== FOYDALANUVCHI MA'LUMOTLARINI QABUL QILISH (TEXT) ==============
async def handle_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(update.message.from_user.id)

    # Har safar xabar kelganda last_activity yangilanadi
    if str_id not in bot_data:
        # agar /start qilmagan bo‘lsa
        bot_data[str_id] = {
            "lang": None,
            "age": None,
            "height": None,
            "weight": None,
            "last_activity": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        save_data(bot_data)
        await update.message.reply_text("Iltimos, avval /start ni bosing.")
        return
    else:
        bot_data[str_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(bot_data)

    lang = bot_data[str_id]["lang"]
    if not lang:
        await update.message.reply_text("Iltimos, /start dan boshlang (til tanlanmagan).")
        return

    try:
        age, height, weight = map(int, update.message.text.replace(' ', '').split(','))
        bot_data[str_id]["age"] = age
        bot_data[str_id]["height"] = height
        bot_data[str_id]["weight"] = weight
        # last_activity ham yangilab bo‘ldik
        save_data(bot_data)

        # BMI, BMR, suv hisobi
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        # Pastki formula erkaklar uchun (agar ayol bo‘lsa o‘zgartirish kerak bo‘ladi)
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
        daily_water_liters = weight * 30 / 1000

        bmi_status_text = {
            'uz': (
                "Sizning vazningiz kam. Vazn olish tavsiya etiladi.🙂" if bmi < 18.5 else
                "Sizning vazningiz sog'lom darajada.☺️" if 18.5 <= bmi < 24.9 else
                "Sizning vazningiz yuqori. Vazn yo'qotish tavsiya etiladi.🙃" if 25 <= bmi < 29.9 else
                "Sizda ortiqcha vazn bor. Mutaxassisga murojaat qiling.😌"
            ),
            'ru': (
                "Ваш вес недостаточный. Рекомендуется набрать вес.🙂" if bmi < 18.5 else
                "Ваш вес в норме.☺️" if 18.5 <= bmi < 24.9 else
                "Ваш вес выше нормы. Рекомендуется похудеть.🙃" if 25 <= bmi < 29.9 else
                "У вас лишний вес. Обратитесь к специалисту.😌"
            ),
            'en': (
                "Your weight is below normal. Weight gain is recommended.🙂" if bmi < 18.5 else
                "Your weight is in the healthy range.☺️" if 18.5 <= bmi < 24.9 else
                "Your weight is above normal. Weight loss is recommended.🙃" if 25 <= bmi < 29.9 else
                "You are overweight. Consult a specialist.😌"
            )
        }

        harmful_text = {
            'uz': (
                "Zararli ichimlik va taomlardan saqlaning:🤗\n"
                "- Shirin gazlangan ichimliklar\n"
                "- Spirtli ichimliklar\n"
                "- Juda yog'li va qovurilgan ovqatlar\n"
                "- Ortiqcha tuz va shakar\n\n"
                "Foydali odatlar:\n"
                "- Oddiy suv ichish\n"
                "- Ko'katlar va mevalar\n"
                "- Sog'lom yog'lar (zaytun moyi va h.k)."
            ),
            'ru': (
                "Избегайте вредных напитков и пищи:🤗\n"
                "- Сладкая газировка\n"
                "- Алкоголь\n"
                "- Жирная и жареная еда\n"
                "- Избыток соли и сахара\n\n"
                "Полезные привычки:\n"
                "- Пить простую воду\n"
                "- Есть зелень и фрукты\n"
                "- Полезные масла (оливковое и т.п.)."
            ),
            'en': (
                "Avoid harmful drinks and foods:🤗\n"
                "- Sugary fizzy drinks\n"
                "- Alcohol\n"
                "- Fatty and fried foods\n"
                "- Too much salt and sugar\n\n"
                "Healthy habits:\n"
                "- Drink plain water\n"
                "- Eat greens and fruits\n"
                "- Healthy oils (olive oil, etc.)."
            )
        }

        summary_text = {
            'uz': f"Sizning BMI: 😊{bmi:.2f}. {bmi_status_text[lang]}\n"
                  f"Kunlik kaloriya ehtiyojingiz (BMR): {bmr:.2f} kkal.\n"
                  f"Kunlik suv iste'moli: {daily_water_liters:.1f} litr.\n\n"
                  f"{harmful_text[lang]}",
            'ru': f"Ваш ИМТ: 😊{bmi:.2f}. {bmi_status_text[lang]}\n"
                  f"Суточная норма калорий (BMR): {bmr:.2f} ккал.\n"
                  f"Рекомендуемое количество воды: {daily_water_liters:.1f} литра.\n\n"
                  f"{harmful_text[lang]}",
            'en': f"Your BMI: 😊{bmi:.2f}. {bmi_status_text[lang]}\n"
                  f"Daily calorie needs (BMR): {bmr:.2f} kcal.\n"
                  f"Daily water intake: {daily_water_liters:.1f} liters.\n\n"
                  f"{harmful_text[lang]}"
        }

        full_text = summary_text[lang]
        if len(full_text) > 3500:
            await send_long_text_in_chunks(full_text, update.effective_chat.id, context)
        else:
            await update.message.reply_text(full_text)

        # Maqsad tanlash tugmalari
        goal_buttons = {
            'uz': ["👉Vazn olish👈", "👉Vazn yo'qotish👈", "👉Vazn saqlash👈"],
            'ru': ["👉Набрать вес👈", "👉Похудеть👈", "👉Сохранить вес👈"],
            'en': ["👉Gain weight👈", "👉Lose weight👈", "👉Maintain weight👈"]
        }
        g_btns = goal_buttons[lang]
        keyboard = [
            [InlineKeyboardButton(g_btns[0], callback_data='goal_gain')],
            [InlineKeyboardButton(g_btns[1], callback_data='goal_lose')],
            [InlineKeyboardButton(g_btns[2], callback_data='goal_maintain')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        choose_text = {
            'uz': "Maqsadingizni tanlang:👇",
            'ru': "Выберите цель:👇",
            'en': "Choose your goal:👇"
        }
        await update.message.reply_text(choose_text[lang], reply_markup=reply_markup)

    except ValueError:
        errors = {
            'uz': "Format xato. (Misol: 25, 175, 70).",
            'ru': "Неверный формат. (Например: 25, 175, 70).",
            'en': "Invalid format. (Example: 25, 175, 70)."
        }
        await update.message.reply_text(errors[lang])


# ============== Maqsad tanlash callback ==============
async def goal_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    goal_type = query.data.split('_')[1]  # gain, lose, maintain

    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(query.from_user.id)
    # har safar callback kelganda ham last_activity yangilanadi
    if str_id in bot_data:
        bot_data[str_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(bot_data)

    lang = bot_data[str_id].get("lang", "uz")
    exercises_info = {
        'gain': {
            'uz': ("🤗Mashg'ulot: Kuch mashg'ulotlari (gantel, og'irliklar):\n"
                   "- Foyda: Mushaklarni kuchaytiradi, vaznni ko'paytiradi.\n"
                   "- Vaqt: 30-40 daqiqa har kuni, haftada 4-5 kun.\n"
                   "- Kaloriya sarfi: ~150-200 kkal (30 daqiqada).\n"
                   "- Ehtiyotkorlik: Bel og'rig'i bo'lganlar ehtiyot bo'lsin.\n"
                   "Quyida foydali taomlarning retseptlari berilgan. Ko'rish uchun 'Taomlar retsepti' tugmasini bosing."),
            'ru': ("🤗Силовые тренировки (гантели, штанга):\n"
                   "- Польза: Укрепляет мышцы, способствует набору веса.\n"
                   "- Время: 30-40 минут в день, 4-5 раз в неделю.\n"
                   "- Калории: ~150-200 ккал за 30 мин.\n"
                   "- Осторожность: При боли в спине будьте внимательны.\n"
                   "Ниже приведены рецепты полезных блюд. Нажмите кнопку «Рецепты блюд» — чтобы их посмотреть."),
            'en': ("🤗Strength training (dumbbells, weights):\n"
                   "- Benefit: Builds muscle, increases weight.\n"
                   "- Time: 30-40 min daily, 4-5 times/week.\n"
                   "- Calories: ~150-200 kcal in 30 min.\n"
                   "- Caution: Watch out for back pain.\n"
                   "Below are recipes for healthy dishes. Click the 'Dish Recipes' button to view them.")
        },
        'lose': {
            'uz': ("🤗Mashg'ulot: Kardio (yugurish, velosiped):\n"
                   "- Foyda: Yog'ni yo'qotadi, yurakni kuchaytiradi.\n"
                   "- Vaqt: 40-60 daqiqa kuniga, haftada 5-6 kun.\n"
                   "- Kaloriya sarfi: ~250-300 kkal (30 daq).\n"
                   "- Ehtiyotkorlik: Yurak muammosi bo'lganlar ehtiyot bo'lsin.\n"
                   "Quyida foydali taomlarning retseptlari..."),
            'ru': ("🤗Кардио (бег, велосипед):\n"
                   "- Сжигает жир, укрепляет сердце.\n"
                   "- 40-60 мин в день, 5-6 раз в неделю.\n"
                   "- Калории: ~250-300 ккал за 30 мин.\n"
                   "- Осторожность: при сердечных болезнях — аккуратно.\n"
                   "Ниже — рецепты полезных блюд..."),
            'en': ("🤗Cardio (running, cycling):\n"
                   "- Burns fat, improves heart health.\n"
                   "- 40-60 min/day, 5-6 days/week.\n"
                   "- ~250-300 kcal per 30 min.\n"
                   "- Caution: heart conditions.\n"
                   "Below are recipes for healthy dishes...")
        },
        'maintain': {
            'uz': ("🤗Kombinatsion mashg'ulotlar (kardio+kuch):\n"
                   "- Foyda: Vaznni saqlaydi.\n"
                   "- 30-40 daqiqa kuniga, 4-5 kun/hafta.\n"
                   "- ~200-250 kkal(30 daqiqa).\n"
                   "- Ehtiyotkorlik: Yaxshi dam olish.\n"
                   "Quyida foydali taomlarning retseptlari..."),
            'ru': ("🤗Комбинированная тренировка (кардио+силовые):\n"
                   "- Помогает держать вес.\n"
                   "- 30-40 мин в день, 4-5 раз в неделю.\n"
                   "- ~200-250 ккал за 30 мин.\n"
                   "- Отдых обязателен.\n"
                   "Ниже — рецепты полезных блюд..."),
            'en': ("🤗Combination (cardio+strength):\n"
                   "- Maintains weight.\n"
                   "- 30-40 min/day, 4-5 times/week.\n"
                   "- ~200-250 kcal/30 min.\n"
                   "- Ensure rest.\n"
                   "Below are recipes for healthy dishes...")
        }
    }

    text_to_send = exercises_info[goal_type][lang]

    recipe_button = {
        'uz': "👉Taomlar retsepti👈",
        'ru': "👉Рецепты блюд👈",
        'en': "👉Recipes👈"
    }

    keyboard = [[InlineKeyboardButton(recipe_button[lang], callback_data='recipes')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=text_to_send, reply_markup=reply_markup)


# ============== "Taomlar retsepti" tugmasi bosilganda ==============
async def recipes_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(query.from_user.id)
    if str_id in bot_data:
        bot_data[str_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(bot_data)

    await show_main_taomlar_menu(update, context)


# ============== ASOSIY TAOMLAR MENYUSI ==============
async def show_main_taomlar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    bot_data = context.bot_data.setdefault("users_db", load_data())

    str_id = str(query.from_user.id)
    lang = bot_data[str_id].get("lang", "uz")

    if query and query.data == 'recipes':
        # callback kelgan, last_activity yangilash
        bot_data[str_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(bot_data)

    text_dict = {
        'uz': "Taomlar bo‘limi. Qaysi bo‘limni tanlaysiz?🤔",
        'ru': "Раздел блюд. Какое выберете?🤔",
        'en': "Dish categories. Which do you choose?🤔"
    }

    keyboard = [
        [InlineKeyboardButton("Suyuq taomlar🍲", callback_data='cat_suyuq')],
        [InlineKeyboardButton("Quyuq taomlar🍝", callback_data='cat_quyuq')],
        [InlineKeyboardButton("Salatlar🥗", callback_data='cat_salatlar')],
        [InlineKeyboardButton("Pishiriqlar🥧", callback_data='cat_pishiriqlar')],
        [InlineKeyboardButton("Shirinliklar🍩", callback_data='cat_shirinliklar')],
        [InlineKeyboardButton("Ichimliklar🍹", callback_data='cat_ichimliklar')],
        [InlineKeyboardButton("Tortlar🍰", callback_data='cat_tortlar')],
        [InlineKeyboardButton("Nonlar🍞", callback_data='cat_nonlar')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=text_dict.get(lang, text_dict['uz']), reply_markup=reply_markup)


# ============== Kategoriya tanlash cat_suyuq, cat_quyuq, ... ==============
async def show_dish_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat = query.data.split('_')[1]  # suyuq, quyuq, salatlar,...

    await show_dish_categories_logic(cat, query, context)


async def show_dish_categories_logic(cat: str, query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(query.from_user.id)
    # last_activity
    if str_id in bot_data:
        bot_data[str_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(bot_data)

    lang = bot_data[str_id].get("lang", "uz")

    category_titles = {
        'uz': {
            'suyuq': "Suyuq taomlar:🍲",
            'quyuq': "Quyuq taomlar:🍝",
            'salatlar': "Salatlar:🥗",
            'pishiriqlar': "Pishiriqlar:🥧",
            'shirinliklar': "Shirinliklar:🍩",
            'ichimliklar': "Ichimliklar:🍹",
            'tortlar': "Tortlar:🍰",
            'nonlar': "Nonlar:🍞"
        },
        'ru': {
            'suyuq': "Супы:🍲",
            'quyuq': "Вторые блюда:🍝",
            'salatlar': "Салаты:🥗",
            'pishiriqlar': "Выпечка:🥧",
            'shirinliklar': "Десерты:🍩",
            'ichimliklar': "Напитки:🍹",
            'tortlar': "Торты:🍰",
            'nonlar': "Хлеб:🍞"
        },
        'en': {
            'suyuq': "Soups:🍲",
            'quyuq': "Stews:🍝",
            'salatlar': "Salads:🥗",
            'pishiriqlar': "Baked goods:🥧",
            'shirinliklar': "Desserts:🍩",
            'ichimliklar': "Drinks:🍹",
            'tortlar': "Cakes:🍰",
            'nonlar': "Breads:🍞"
        }
    }

    # Turli keyboard variantlari:
    if cat == "suyuq":
        text_label = category_titles[lang]['suyuq']
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
        text_label = category_titles[lang]['quyuq']
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
        text_label = category_titles[lang]['salatlar']
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
        text_label = category_titles[lang]['pishiriqlar']
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
        text_label = category_titles[lang]['shirinliklar']
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
        text_label = category_titles[lang]['ichimliklar']
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
        text_label = category_titles[lang]['tortlar']
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
        text_label = category_titles[lang]['nonlar']
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



# ============== Retsept callback: dish_..., drink_..., tort_..., non_, ... ==============

# <-- O'ZGARTIRILGAN (1) -->
# Bu yerda matn + rasm yuborganda, ularning message_id larini saqlaymiz
async def show_recipe_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data_key = query.data

    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(query.from_user.id)
    if str_id in bot_data:
        bot_data[str_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(bot_data)

    text_data = recipes_texts.get(data_key, "Bu taom (yoki ichimlik) bo'yicha ma'lumot topilmadi.")
    image_path = images_paths.get(data_key)

    # "Ortga" tugmasi
    keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data='back_to_taomlar')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # RASM yuborish
    photo_message_id = None
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as img_file:
                sent_photo_msg = await context.bot.send_photo(
                    chat_id=query.from_user.id,
                    photo=img_file
                )
                photo_message_id = sent_photo_msg.message_id  # saqlab qo'yamiz
        except Exception as e:
            logger.error(f"Rasm yuborishda xatolik: {e}")
            await context.bot.send_message(chat_id=query.from_user.id, text="Rasm yuborishda xatolik yuz berdi.")
    else:
        logger.warning(f"Rasm topilmadi: {image_path}")

    # MATN yuborish
    text_message_id = None
    if len(text_data) > 3500:
        await send_long_text_in_chunks(text_data, query.from_user.id, context)
        msg = await context.bot.send_message(
            chat_id=query.from_user.id,
            text="...",
            reply_markup=reply_markup
        )
        text_message_id = msg.message_id
    else:
        msg = await context.bot.send_message(
            chat_id=query.from_user.id,
            text=text_data,
            reply_markup=reply_markup
        )
        text_message_id = msg.message_id

    # Xabar ID larini user_data ga yozamiz
    context.user_data['recipe_photo_msg_id'] = photo_message_id
    context.user_data['recipe_text_msg_id'] = text_message_id


# ============== Ortga "taomlar" ==============

# <-- O'ZGARTIRILGAN (2) -->
# Ortga bosilganda avval rasm + matn xabarini o'chiramiz, so'ng asosiy menyu ko'rsatamiz
async def back_to_taomlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Avval yuborilgan rasm xabarini o'chiramiz
    photo_msg_id = context.user_data.get('recipe_photo_msg_id')
    if photo_msg_id:
        try:
            await context.bot.delete_message(chat_id=query.from_user.id, message_id=photo_msg_id)
        except Exception as e:
            logger.error(f"Rasm xabarni o'chirishda xatolik: {e}")
        context.user_data.pop('recipe_photo_msg_id', None)

    # Matn xabarini o'chiramiz
    text_msg_id = context.user_data.get('recipe_text_msg_id')
    if text_msg_id:
        try:
            await context.bot.delete_message(chat_id=query.from_user.id, message_id=text_msg_id)
        except Exception as e:
            logger.error(f"Matn xabarni o'chirishda xatolik: {e}")
        context.user_data.pop('recipe_text_msg_id', None)

    # Endi asosiy taomlar menyusiga qaytamiz
    await show_main_taomlar_menu(update, context)

    # last_activity
    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(query.from_user.id)
    if str_id in bot_data:
        bot_data[str_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(bot_data)



# ============== Ortga kategoriya: Agar keraksiz bo‘lsa, soddalashtirilgan... ==============
#  shu loyihada ortga kategoriya emas, bevosita "taomlar"ga qaytyapmiz.


# ============== 1) /users — faqat so‘nggi 30 kunda aktiv va chatdan chiqmaganlar soni ==============
async def user_count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data.setdefault("users_db", load_data())

    # Admin bo‘lmasayam kimdir /users ni bosishi mumkin. Ruxsat berilsa bo‘ldi, cheklash shart emas.
    # Agar cheklamoqchi bo‘lsak, admin tekshirish qilamiz.

    active_count = 0
    now = datetime.now()

    # Har bir foydalanuvchi uchun tekshiramiz
    user_ids = list(bot_data.keys())
    fail_count = 0
    for uid in user_ids:
        user_info = bot_data[uid]
        last_active_str = user_info.get("last_activity")
        if not last_active_str:
            continue  # hech qachon /start qilmagan bo‘lishi mumkin
        try:
            last_active_dt = datetime.strptime(last_active_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue

        # 30 kundan oshiq bo'lsa skip
        if (now - last_active_dt) > timedelta(days=30):
            continue

        # chatdan chiqib ketganmi tekshiramiz
        try:
            uid_int = int(uid)
            member = await context.bot.get_chat_member(uid_int, uid_int)
            if member.status not in ("left", "kicked"):
                # demak botni o‘chirib tashlamagan
                active_count += 1
        except Exception as e:
            # get_chat_member xato bersa, balki user blocked the bot
            logger.error(f"get_chat_member failed for {uid}: {e}")
            fail_count += 1

    msg_text = (
        f"Faol foydalanuvchilar (so‘nggi 30 kunda), botni tark etmaganlar soni: {active_count}\n"
        f"(Tekshirishda xato chiqqan userlar: {fail_count} ta)"
    )
    await update.message.reply_text(msg_text)


# ============== 2) /admin_broadcast — faqat adminlarga ruxsat. Xabarni forward (yoki copy) qilib yuboradi ==============
async def admin_broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ADMIN_IDS:
        await update.message.reply_text("Ushbu buyruq faqat admin uchun.")
        return

    # Admin xabarni reply shaklida yuborishi kutiladi. Tekshiruv
    if not update.message.reply_to_message:
        await update.message.reply_text("Iltimos, reply (javob) tarzida xabar yoki media ustiga /admin_broadcast yuboring.")
        return

    bot_data = context.bot_data.setdefault("users_db", load_data())

    broadcast_count = 0
    fail_count = 0

    for uid_str in bot_data.keys():
        try:
            # forward
            await context.bot.copy_message(
                chat_id=int(uid_str),
                from_chat_id=update.effective_chat.id,
                message_id=update.message.reply_to_message.message_id
            )
            broadcast_count += 1
        except Exception as e:
            logger.error(f"Broadcast to {uid_str} failed: {e}")
            fail_count += 1

    await update.message.reply_text(
        f"Xabar forward qilindi. Muvaffaqiyatli: {broadcast_count} ta. Xato: {fail_count} ta."
    )


# ============== BOTGA KOMANDALAR VA CALLBACKLARNI QO‘SHISH ==============
def main():
    # Webhook URL
    HEROKU_APP_NAME = "hayotbalansibot"  # Heroku ilovangiz nomini kiriting
    WEBHOOK_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/{BOT_TOKEN}"
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # /start komandasi
    application.add_handler(CommandHandler("start", start))

    # Til tanlash callback
    application.add_handler(CallbackQueryHandler(language_selection, pattern='^lang_(uz|ru|en)$'))

    # Foydalanuvchi matn (age,height,weight) kiritsa
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_data))

    # Maqsad tanlash
    application.add_handler(CallbackQueryHandler(goal_selection, pattern='^goal_(gain|lose|maintain)$'))

    # "Taomlar retsepti" tugmasi => recipes
    application.add_handler(CallbackQueryHandler(recipes_button_handler, pattern='^recipes$'))

    # Bo‘limga kirish: cat_suyuq, cat_quyuq, ...
    application.add_handler(CallbackQueryHandler(show_dish_categories, pattern='^cat_'))

    # Retsept callback: dish_..., drink_..., tort_..., non_, ...
    application.add_handler(CallbackQueryHandler(show_recipe_callback, pattern='^(dish_|drink_|tort_|non_).*'))

    # Ortga "taomlar" menu
    application.add_handler(CallbackQueryHandler(back_to_taomlar, pattern='^back_to_taomlar$'))

    # /users
    application.add_handler(CommandHandler("users", user_count_command))

    # /admin_broadcast
    application.add_handler(CommandHandler("admin_broadcast", admin_broadcast_command))

    # Start Webhook
    port = int(os.environ.get("PORT", "8443"))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=BOT_TOKEN,
        webhook_url=WEBHOOK_URL,
    )


if __name__ == '__main__':
    main()
