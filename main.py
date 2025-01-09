import os
import logging
import json
from datetime import datetime, timedelta
from images_paths import images_paths
from recipes_texts import recipes_texts
from flask import Flask, request

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
from dotenv import load_dotenv

# .env fayldan o‘zgaruvchilarni yuklash
load_dotenv()

# Flask ilovasini yaratish
app = Flask(__name__)

# ============== LOGGER (log) sozlamalari ==============
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
# O'zgaruvchilarni yuklash
BOT_TOKEN = os.environ.get("BOT_TOKEN")
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
PORT = int(os.environ.get("PORT", "8443"))
HEROKU_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN o'rnatilmagan yoki noto'g'ri. Iltimos, .env faylda uni tekshiring.")


# ============== ADMIN IDs ==============
ADMIN_IDS = [7465094605]  # <-- O'zingizning telegram ID raqamingiz

# ============== GLOBAL o'zgaruvchilar ==============
DATA_FILE = "data.json"  # foydalanuvchi ma’lumotlari saqlanadigan fayl

# ============== JSON orqali ma’lumotlarni saqlash/yuklash ==============
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data: dict):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============== Yordamchi funksiyalar ==============
async def send_long_text_in_chunks(text, chat_id, context, chunk_size=3500):
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
    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(chat_id)
    if str_id not in bot_data:
        bot_data[str_id] = {
            "lang": None,
            "age": None,
            "height": None,
            "weight": None,
            "last_activity": None,
        }
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
    lang = query.data.split('_')[1]
    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(query.from_user.id)
    if str_id in bot_data:
        bot_data[str_id]["lang"] = lang
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
    if str_id not in bot_data:
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
        save_data(bot_data)

        height_m = height / 100
        bmi = weight / (height_m ** 2)
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
        daily_water_liters = weight * 30 / 1000

        # ============== WEBHOOK SOZLASH ==============
        # Webhook marshrutini sozlash
        @app.route(f"/{os.environ.get('BOT_TOKEN')}", methods=["POST"])
        def webhook():
            update = Update.de_json(request.get_json(force=True), application.bot)
            application.update_queue.put(update)
            return "ok"
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
    goal_type = query.data.split('_')[1]

    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(query.from_user.id)
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

# ============== Kategoriya tanlash ==============
async def show_dish_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat = query.data.split('_')[1]
    await show_dish_categories_logic(cat, query, context)

async def show_dish_categories_logic(cat: str, query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(query.from_user.id)
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
    # Boshqa kategoriyalar uchun ham xuddi shunday qo'shishingiz mumkin...
    else:
        text_label = "Noma'lum bo‘lim."
        keyboard = [[InlineKeyboardButton("Ortga⬅️", callback_data='back_to_taomlar')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text_label, reply_markup=reply_markup)

# ============== Retsept callback ==============
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

    context.user_data['recipe_photo_msg_id'] = photo_message_id
    context.user_data['recipe_text_msg_id'] = text_message_id

# ============== Ortga "taomlar" ==============
async def back_to_taomlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    bot_data = context.bot_data.setdefault("users_db", load_data())
    str_id = str(query.from_user.id)
    if str_id in bot_data:
        bot_data[str_id]["last_activity"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data(bot_data)

# ============== /users komanda ==============
async def user_count_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_data = context.bot_data.setdefault("users_db", load_data())
    active_count = 0
    now = datetime.now()
    user_ids = list(bot_data.keys())
    fail_count = 0
    for uid in user_ids:
        user_info = bot_data[uid]
        last_active_str = user_info.get("last_activity")
        if not last_active_str:
            continue
        try:
            last_active_dt = datetime.strptime(last_active_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        if (now - last_active_dt) > timedelta(days=30):
            continue
        try:
            uid_int = int(uid)
            member = await context.bot.get_chat_member(uid_int, uid_int)
            if member.status not in ("left", "kicked"):
                active_count += 1
        except Exception as e:
            logger.error(f"get_chat_member failed for {uid}: {e}")
            fail_count += 1

    msg_text = (
        f"Faol foydalanuvchilar (so‘nggi 30 kunda), botni tark etmaganlar soni: {active_count}\n"
        f"(Tekshirishda xato chiqqan userlar: {fail_count} ta)"
    )
    await update.message.reply_text(msg_text)

# ============== /admin_broadcast komanda ==============
async def admin_broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("Ushbu buyruq faqat admin uchun.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Iltimos, reply (javob) tarzida xabar yoki media ustiga /admin_broadcast yuboring.")
        return

    bot_data = context.bot_data.setdefault("users_db", load_data())
    broadcast_count = 0
    fail_count = 0
    for uid_str in bot_data.keys():
        try:
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
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com"

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_selection, pattern='^lang_(uz|ru|en)$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_data))
    application.add_handler(CallbackQueryHandler(goal_selection, pattern='^goal_(gain|lose|maintain)$'))
    application.add_handler(CallbackQueryHandler(recipes_button_handler, pattern='^recipes$'))
    application.add_handler(CallbackQueryHandler(show_dish_categories, pattern='^cat_'))
    application.add_handler(CallbackQueryHandler(show_recipe_callback, pattern='^(dish_|drink_|tort_|non_).*'))
    application.add_handler(CallbackQueryHandler(back_to_taomlar, pattern='^back_to_taomlar$'))
    application.add_handler(CommandHandler("users", user_count_command))
    application.add_handler(CommandHandler("admin_broadcast", admin_broadcast_command))

    logger.info("Bot ishga tushirildi...")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{HEROKU_URL}/{BOT_TOKEN}"
    )

if __name__ == '__main__':
    main()
