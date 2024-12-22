# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters, JobQueue
)
from datetime import time

# Global variables
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

        # Calculate BMI
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        user_data[user_id]['bmi'] = bmi

        # Calculate daily calorie needs (BMR for men)
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
        user_data[user_id]['calories'] = bmr

        # Calculate daily water intake
        daily_water_ml = weight * 30
        daily_water_liters = daily_water_ml / 1000
        user_data[user_id]['water'] = daily_water_liters

        # BMI Category
        if bmi < 18.5:
            bmi_status = "Sizning vazningiz kam. Vazn olish tavsiya etiladi."
        elif 18.5 <= bmi < 24.9:
            bmi_status = "Sizning vazningiz sog'lom darajada."
        elif 25 <= bmi < 29.9:
            bmi_status = "Sizning vazningiz yuqori. Vazn yo'qotish tavsiya etiladi."
        else:
            bmi_status = "Sizda ortiqcha vazn bor. Mutaxassisga murojaat qiling."

        # Messages for the user
        messages = {
            'uz': (f"Sizning BMI: {bmi:.2f}. {bmi_status}\n"
                   f"Kunlik kaloriya ehtiyojingiz: {bmr:.2f} kkal.\n"
                   f"Kunlik suv iste'moli: {daily_water_liters:.1f} litr.\n"
                   "Endi maqsadingizni tanlang:"),
            'ru': (f"Ваш ИМТ: {bmi:.2f}. {bmi_status}\n"
                   f"Ваши суточные калории: {bmr:.2f} ккал.\n"
                   f"Рекомендуемое количество воды: {daily_water_liters:.1f} литра.\n"
                   "Теперь выберите вашу цель:"),
            'en': (f"Your BMI: {bmi:.2f}. {bmi_status}\n"
                   f"Daily calorie needs: {bmr:.2f} kcal.\n"
                   f"Daily water intake: {daily_water_liters:.1f} liters.\n"
                   "Now choose your goal:")
        }

        # Dynamic buttons
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
        await update.message.reply_text("Noto'g'ri format. Iltimos, yosh, bo'y va vaznni to'g'ri formatda kiriting.")


# Goal selection handler
async def goal_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    goal = query.data
    user_id = query.from_user.id
    user_data[user_id]['goal'] = goal

    lang = user_data[user_id]['lang']
    weight = user_data[user_id]['weight']
    calories = user_data[user_id]['calories']
    water = user_data[user_id]['water']

    # Sport recommendations
    exercises = {
        'gain': {
            'uz': ("Mashg'ulot: Kuch mashg'ulotlari (gantel va og'irliklar bilan ishlash):\n"
                   "- Foyda: Mushaklarni kuchaytiradi va vaznni ko'paytiradi.\n"
                   "- Vaqt: 30-40 daqiqa har kuni, haftada 4-5 kun.\n"
                   "- Kaloriya sarfi: Har 30 daqiqada ~150-200 kkal."),
            'ru': ("Тренировка: Силовые тренировки (работа с гантелями и весами):\n"
                   "- Польза: Укрепляет мышцы и способствует набору веса.\n"
                   "- Время: 30-40 минут каждый день, 4-5 раз в неделю.\n"
                   "- Расход калорий: ~150-200 ккал за 30 минут."),
            'en': ("Workout: Strength training (working with dumbbells and weights):\n"
                   "- Benefits: Strengthens muscles and promotes weight gain.\n"
                   "- Time: 30-40 minutes daily, 4-5 days a week.\n"
                   "- Calories burned: ~150-200 kcal per 30 minutes.")
        },
        'lose': {
            'uz': ("Mashg'ulot: Kardio mashg'ulotlari (yugurish, velosipedda yurish):\n"
                   "- Foyda: Yog'larni yo'qotadi va yurak salomatligini yaxshilaydi.\n"
                   "- Vaqt: 40-60 daqiqa har kuni, haftada 5-6 kun.\n"
                   "- Kaloriya sarfi: Har 30 daqiqada ~250-300 kkal."),
            'ru': ("Тренировка: Кардио тренировки (бег, велоспорт):\n"
                   "- Польза: Сжигает жиры и улучшает здоровье сердца.\n"
                   "- Время: 40-60 минут ежедневно, 5-6 раз в неделю.\n"
                   "- Расход калорий: ~250-300 ккал за 30 минут."),
            'en': ("Workout: Cardio exercises (running, cycling):\n"
                   "- Benefits: Burns fat and improves heart health.\n"
                   "- Time: 40-60 minutes daily, 5-6 days a week.\n"
                   "- Calories burned: ~250-300 kcal per 30 minutes.")
        },
        'maintain': {
            'uz': ("Mashg'ulot: Kombinatsion mashg'ulotlar (kardio + kuch mashqlari):\n"
                   "- Foyda: Vaznni barqaror saqlashga yordam beradi.\n"
                   "- Vaqt: 30-40 daqiqa har kuni, haftada 4-5 kun.\n"
                   "- Kaloriya sarfi: Har 30 daqiqada ~200-250 kkal."),
            'ru': ("Тренировка: Комбинированные тренировки (кардио + силовые):\n"
                   "- Польза: Помогает поддерживать стабильный вес.\n"
                   "- Время: 30-40 минут ежедневно, 4-5 раз в неделю.\n"
                   "- Расход калорий: ~200-250 ккал за 30 минут."),
            'en': ("Workout: Combination training (cardio + strength):\n"
                   "- Benefits: Helps maintain stable weight.\n"
                   "- Time: 30-40 minutes daily, 4-5 times a week.\n"
                   "- Calories burned: ~200-250 kcal per 30 minutes.")
        }
    }

    message = exercises[goal][lang]
    await query.edit_message_text(f"{message}\n\nKunlik kaloriya ehtiyojingiz: {calories:.2f} kkal.\n"
                                  f"Kunlik suv iste'moli: {water:.1f} litr.")


# Reminder function
async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.context['chat_id']
    lang = user_data[job.context['user_id']]['lang']
    reminders = {
        'uz': "Eslatma: Suv ichishni unutmang! Mashg'ulot qiling va sog'lom turmush tarzini saqlang! 💧🏋️‍♂️",
        'ru': "Напоминание: Не забудьте пить воду! Тренируйтесь и ведите здоровый образ жизни! 💧🏋️‍♂️",
        'en': "Reminder: Don't forget to drink water! Exercise and maintain a healthy lifestyle! 💧🏋️‍♂️"
    }
    await context.bot.send_message(chat_id=chat_id, text=reminders[lang])


# Set daily reminders
async def set_daily_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        await update.message.reply_text("Iltimos, /start buyruğidan boshlang.")
        return

    context.job_queue.run_daily(
        send_reminder,
        time=time(9, 0),  # Reminder at 9:00 AM
        context={'chat_id': update.message.chat_id, 'user_id': user_id}
    )
    await update.message.reply_text("Kunlik eslatmalar muvaffaqiyatli o‘rnatildi!")


# Main function to start the bot
def main():
    application = ApplicationBuilder().token("8018294597:AAF5quzQeBXzhYInX5NVlujcJ3TrPYhnmZQ").build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(language_selection, pattern='^(uz|ru|en)$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_data))
    application.add_handler(CallbackQueryHandler(goal_selection, pattern='^(gain|lose|maintain)$'))
    application.add_handler(CommandHandler("set_reminders", set_daily_reminders))

    # Run the bot
    application.run_polling()


if __name__ == '__main__':
    main()
