from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
user_data = {}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = ("Assalomu alaykum!☺️☺️ Sog'lom turmush tarzini targ'ib qiluvchi botga xush kelibsiz! "
            "Iltimos, o'zingizga qulay tilni tanlang.\n"
            "Ассаламу алайкум!☺️☺️ Добро пожаловать в бота, продвигающего здоровый образ жизни! "
            "Пожалуйста, выберите удобный для вас язык.\n"
            "Assalamu alaykum!☺️☺️ Welcome to the bot promoting a healthy lifestyle! Please select your preferred language.")
    keyboard = [
        [InlineKeyboardButton("O'zbekcha", callback_data='uz'),
         InlineKeyboardButton("Русский", callback_data='ru'),
         InlineKeyboardButton("English", callback_data='en')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

# Language selection handler
async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data
    user_data[query.from_user.id] = {'lang': lang}
    messages = {
        'uz': "Til tanlandi: O'zbekcha. Keling, boshlaymiz! Yosh, bo'yingiz (sm) va vazningizni (kg) kiriting (masalan: 25, 175, 70).",
        'ru': "Вы выбрали русский язык. Давайте начнём! Введите ваш возраст, рост (см) и вес (кг) (например: 25, 175, 70).",
        'en': "You selected English. Let's start! Please enter your age, height (cm), and weight (kg) (e.g., 25, 175, 70)."
    }
    await query.edit_message_text(text=messages[lang])

# User input handler
async def handle_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        await update.message.reply_text("Iltimos, /start buyruğidan boshlang.")
        return

    lang = user_data[user_id]['lang']
    try:
        age, height, weight = map(int, update.message.text.split(','))
        user_data[user_id].update({'age': age, 'height': height, 'weight': weight})

        # Calculate BMI, daily calories, and water intake
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
        daily_water_liters = weight * 30 / 1000

        bmi_status = {
            'uz': ("Sizning vazningiz kam. Vazn olish tavsiya etiladi." if bmi < 18.5 else
                   "Sizning vazningiz sog'lom darajada." if 18.5 <= bmi < 24.9 else
                   "Sizning vazningiz yuqori. Vazn yo'qotish tavsiya etiladi." if 25 <= bmi < 29.9 else
                   "Sizda ortiqcha vazn bor. Mutaxassisga murojaat qiling."),
            'ru': ("Ваш вес недостаточный. Рекомендуется набрать вес." if bmi < 18.5 else
                   "Ваш вес в норме." if 18.5 <= bmi < 24.9 else
                   "Ваш вес выше нормы. Рекомендуется похудеть." if 25 <= bmi < 29.9 else
                   "У вас лишний вес. Обратитесь к специалисту."),
            'en': ("Your weight is below normal. Weight gain is recommended." if bmi < 18.5 else
                   "Your weight is in the healthy range." if 18.5 <= bmi < 24.9 else
                   "Your weight is above normal. Weight loss is recommended." if 25 <= bmi < 29.9 else
                   "You are overweight. Consult a specialist.")
        }
        harmful_items = {
            'uz': ("Zararli ichimliklar va taomlardan saqlaning:\n"
                   "- Shirin gazlangan ichimliklar\n"
                   "- Spirtli ichimliklar\n"
                   "- Haddan tashqari yog'li va qovurilgan ovqatlar\n"
                   "- Ortiqcha tuz va shakar iste'moli\n\n"
                   "Foydali odatlar:\n"
                   "- Oddiy suv iching\n"
                   "- Ko'katlar va mevalar iste'mol qiling\n"
                   "- Sog'lom yog'lar (masalan, zaytun moyi) iste'mol qiling."),
            'ru': ("Избегайте вредных напитков и пищи:\n"
                   "- Сладкие газированные напитки\n"
                   "- Алкогольные напитки\n"
                   "- Жирная и жареная еда\n"
                   "- Избыточное употребление соли и сахара\n\n"
                   "Полезные привычки:\n"
                   "- Пейте чистую воду\n"
                   "- Ешьте зелень и фрукты\n"
                   "- Используйте здоровые жиры (например, оливковое масло)."),
            'en': ("Avoid harmful drinks and foods:\n"
                   "- Sugary fizzy drinks\n"
                   "- Alcoholic beverages\n"
                   "- Excessively fatty and fried foods\n"
                   "- Excessive salt and sugar consumption\n\n"
                   "Healthy habits:\n"
                   "- Drink plain water\n"
                   "- Eat greens and fruits\n"
                   "- Use healthy fats (e.g., olive oil).")
        }
        messages = {
            'uz': f"Sizning BMI: {bmi:.2f}. {bmi_status[lang]}\n"
                  f"Kunlik kaloriya ehtiyojingiz: {bmr:.2f} kkal.\n"
                  f"Kunlik suv iste'moli: {daily_water_liters:.1f} litr.\n\n"
                  f"{harmful_items[lang]}",
            'ru': f"Ваш ИМТ: {bmi:.2f}. {bmi_status[lang]}\n"
                  f"Ваши суточные калории: {bmr:.2f} ккал.\n"
                  f"Рекомендуемое количество воды: {daily_water_liters:.1f} литра.\n\n"
                  f"{harmful_items[lang]}",
            'en': f"Your BMI: {bmi:.2f}. {bmi_status[lang]}\n"
                  f"Daily calorie needs: {bmr:.2f} kcal.\n"
                  f"Daily water intake: {daily_water_liters:.1f} liters.\n\n"
                  f"{harmful_items[lang]}"
        }

        button_texts = {
            'uz': ["Vazn olish", "Vazn yo'qotish", "Vazn saqlash"],
            'ru': ["Набрать вес", "Похудеть", "Сохранить вес"],
            'en': ["Gain weight", "Lose weight", "Maintain weight"]
        }

        buttons = button_texts[lang]
        keyboard = [
            [InlineKeyboardButton(buttons[0], callback_data='gain')],
            [InlineKeyboardButton(buttons[1], callback_data='lose')],
            [InlineKeyboardButton(buttons[2], callback_data='maintain')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(messages[lang], reply_markup=reply_markup)
    except ValueError:
        error_messages = {
            'uz': "Noto'g'ri format. Iltimos, yosh, bo'y va vaznni to'g'ri formatda kiriting.",
            'ru': "Неверный формат. Пожалуйста, введите возраст, рост и вес в правильном формате.",
            'en': "Invalid format. Please enter your age, height, and weight in the correct format."
        }
        await update.message.reply_text(error_messages[lang])

# Goal selection handler
async def goal_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    goal = query.data
    user_id = query.from_user.id
    user_data[user_id]['goal'] = goal

    lang = user_data[user_id]['lang']

    exercises = {
        'gain': {
            'uz': ("Mashg'ulot: Kuch mashg'ulotlari (gantel va og'irliklar bilan ishlash):\n"
                   "- Foyda: Mushaklarni kuchaytiradi va vaznni ko'paytiradi.\n"
                   "- Vaqt: 30-40 daqiqa har kuni, haftada 4-5 kun.\n"
                   "- Kaloriya sarfi: Har 30 daqiqada ~150-200 kkal.\n"
                   "- Ehtiyotkorlik: Bo'g'in yoki bel og'rig'i bo'lganlar uchun mos emas."),
            'ru': ("Тренировка: Силовые тренировки (работа с гантелями и весами):\n"
                   "- Польза: Укрепляет мышцы и способствует набору веса.\n"
                   "- Время: 30-40 минут каждый день, 4-5 раз в неделю.\n"
                   "- Расход калорий: ~150-200 ккал за 30 минут.\n"
                   "- Осторожность: Не подходит для людей с болью в суставах или спине."),
            'en': ("Workout: Strength training (with dumbbells and weights):\n"
                   "- Benefits: Strengthens muscles and promotes weight gain.\n"
                   "- Time: 30-40 minutes daily, 4-5 days a week.\n"
                   "- Calories burned: ~150-200 kcal per 30 minutes.\n"
                   "- Caution: Not suitable for people with joint or back pain.")
        },
        'lose': {
            'uz': ("Mashg'ulot: Kardio mashg'ulotlari (yugurish, velosipedda yurish):\n"
                   "- Foyda: Yog'larni yo'qotadi va yurak salomatligini yaxshilaydi.\n"
                   "- Vaqt: 40-60 daqiqa har kuni, haftada 5-6 kun.\n"
                   "- Kaloriya sarfi: Har 30 daqiqada ~250-300 kkal.\n"
                   "- Ehtiyotkorlik: Yurak kasalligi bo'lganlar ehtiyot bo'lsin."),
            'ru': ("Тренировка: Кардио тренировки (бег, велоспорт):\n"
                   "- Польза: Сжигает жиры и улучшает здоровье сердца.\n"
                   "- Время: 40-60 минут ежедневно, 5-6 раз в неделю.\n"
                   "- Расход калорий: ~250-300 ккал за 30 минут.\n"
                   "- Осторожность: Будьте осторожны, если у вас есть сердечные заболевания."),
            'en': ("Workout: Cardio exercises (running, cycling):\n"
                   "- Benefits: Burns fat and improves heart health.\n"
                   "- Time: 40-60 minutes daily, 5-6 days a week.\n"
                   "- Calories burned: ~250-300 kcal per 30 minutes.\n"
                   "- Caution: Be careful if you have heart conditions.")
        },
        'maintain': {
            'uz': ("Mashg'ulot: Kombinatsion mashg'ulotlar (kardio + kuch mashqlari):\n"
                   "- Foyda: Vaznni barqaror saqlashga yordam beradi.\n"
                   "- Vaqt: 30-40 daqiqa har kuni, haftada 4-5 kun.\n"
                   "- Kaloriya sarfi: Har 30 daqiqada ~200-250 kkal.\n"
                   "- Ehtiyotkorlik: To'g'ri dam olishni unutmang."),
            'ru': ("Тренировка: Комбинированные тренировки (кардио + силовые):\n"
                   "- Польза: Помогает поддерживать стабильный вес.\n"
                   "- Время: 30-40 минут ежедневно, 4-5 раз в неделю.\n"
                   "- Расход калорий: ~200-250 ккал за 30 минут.\n"
                   "- Осторожность: Не забывайте про правильный отдых."),
            'en': ("Workout: Combination training (cardio + strength):\n"
                   "- Benefits: Helps maintain stable weight.\n"
                   "- Time: 30-40 minutes daily, 4-5 days a week.\n"
                   "- Calories burned: ~200-250 kcal per 30 minutes.\n"
                   "- Caution: Ensure proper rest.")
        }
    }

    await query.edit_message_text(exercises[goal][lang])

# Main function to start the bot
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_selection, pattern='^(uz|ru|en)$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_data))
    application.add_handler(CallbackQueryHandler(goal_selection, pattern='^(gain|lose|maintain)$'))
    application.run_polling()

if __name__ == '__main__':
    main()
