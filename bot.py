python
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "7272202729:AAHJtM_2srj5Ave6HQqFcwdAmkZ5Di9jNH0"

FREE_CATEGORY = "Flirty"

CATEGORIES = {
    "1": "Flirty",
    "2": "Naughty Boss",
    "3": "Teacher",
    "4": "Neighbours",
    "5": "Old Man",
    "6": "Old Lady",
    "7": "Just 18",
    "8": "Night Club",
    "9": "Girls Like It Hard",
    "10": "Trios",
    "11": "My Sister",
    "12": "My Dad",
}

LANGUAGES = {
    "en": "English",
    "es": "Espanol",
    "ru": "Russian"
}

user_language = {}
user_category = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='lang_en'),
            InlineKeyboardButton("Espanol", callback_data='lang_es'),
            InlineKeyboardButton("Russian", callback_data='lang_ru'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please select your language / Por favor selecciona tu idioma / Пожалуйста выберите язык:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith('lang_'):
        lang = data.split('_')[1]
        user_language[query.from_user.id] = lang
        await query.edit_message_text(text=f"Idioma seleccionado: {LANGUAGES.get(lang, 'Espanol')}.\nCategoria gratis: {FREE_CATEGORY}")

        keyboard = []
        for key, value in CATEGORIES.items():
            keyboard.append([InlineKeyboardButton(value, callback_data=f"cat_{key}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Please select a category / Por favor selecciona una categoria / Пожалуйста выберите категорию:", reply_markup=reply_markup)

    elif data.startswith('cat_'):
        cat_key = data.split('_')[1]
        user_category[query.from_user.id] = cat_key
        if cat_key == "1":  # Free category
            await query.edit_message_text(text=f"Has seleccionado la categoria gratis: {CATEGORIES[cat_key]}")
        else:
            await query.edit_message_text(text="Esta categoria es premium. Por favor suscribete para acceder.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    cat_key = user_category.get(user_id, "1")

    if cat_key != "1":
        await update.message.reply_text("Esta es una categoria premium. Por favor actualiza tu suscripcion.")
        return

    text = update.message.text.lower()
    # Aqui iria la logica AI para responder, por ahora respuesta dummy
    await update.message.reply_text(f"Respuesta para categoria {CATEGORIES[cat_key]}: {text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()

if name == '_main_':
    main()

