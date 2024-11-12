from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
# Til uchun global o'zgaruvchi
user_language = {}

# Start buyrug'i uchun funksiya
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Inline tugmalarni yaratish
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='uz'),
            InlineKeyboardButton("🇷🇺 Русский", callback_data='ru'),
            InlineKeyboardButton("🇬🇧 English", callback_data='eng')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select language:", reply_markup=reply_markup)

# Tilni tanlagandan keyin xabar yuborish uchun funksiya
async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    language = query.data
    user_language[chat_id] = language

    # Tilga qarab xabar matnini sozlash
    if language == 'uz':
        welcome_text = "Assalomu alaykum Canva Botimizga Xush kelibsiz! Ishni boshlash uchun [Start Project](https://www.canva.com) tugmasini bosing! Tilni o'zgartirish uchun /start ni bosing!!!"
    elif language == 'ru':
        welcome_text = "Добро пожаловать в наш Canva бот! Нажмите на кнопку [Start Project](https://www.canva.com), чтобы начать! Нажмите /start, чтобы изменить язык!!!"
    elif language == 'eng':
        welcome_text = "Welcome to our Canva Bot! Press the [Start Project](https://www.canva.com) button to get started! Press /start to change language!!!"

    await query.edit_message_text(text=welcome_text, parse_mode=ParseMode.MARKDOWN)

# Har qanday boshqa xabar uchun funksiya
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    language = user_language.get(chat_id, 'uz')  # Default til: 'uz'

    # Tilga qarab xabar matnini sozlash
    if language == 'uz':
        error_text = "Noto'g'ri Buyruq, ishni boshlash uchun [Start Project](https://www.canva.com) tugmasini bosing!"
    elif language == 'ru':
        error_text = "Неправильная команда, нажмите на кнопку [Start Project](https://www.canva.com), чтобы начать!"
    elif language == 'eng':
        error_text = "Invalid command, press the [Start Project](https://www.canva.com) button to start!"

    await update.message.reply_text(error_text, parse_mode=ParseMode.MARKDOWN)

# Asosiy bot dasturi
def main():
    app = ApplicationBuilder().token("7639367634:AAGb45ZKVndNQ5CPAvq3flYS7l05XN5vXiA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_selection))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()
