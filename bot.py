```python
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

Variables de entorno
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

Categorías para usuarios premium
CATEGORIES = [
    "Naughty Boss",
    "Teacher",
    "Neighbours",
    "Old Man",
    "Old Lady",
    "Just 18",
    "Night Club",
    "Girls Like It Hard",
    "Trios",
    "Family Roleplay"
]

FREE_CATEGORY = "Free Chat"

LANGUAGES = ["English", "Spanish", "Russian"]

Teclado para idiomas
lang_keyboard = ReplyKeyboardMarkup([LANGUAGES], one_time_keyboard=True, resize_keyboard=True)

Diccionario para guardar usuario premium o no
user_premium = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_premium[user.id] = False  # Por defecto free user
    await update.message.reply_text(
        "Hola! Soy tu bot flirty y divertido.\n"
        "Selecciona idioma / Select language / Выберите язык:",
        reply_markup=lang_keyboard
    )
async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text.lower()
    context.user_data['language'] = lang
    if lang in ['spanish', 'español']:
        await update.message.replay_text(f"Idioma seleccionado: Español.\nCategoría gratis: {FREE_CATEGORY}")
    elif lang == 'russian':
        await update.message.reply_text(f"Выбран язык: Русский.\nБесплатная категория: {FREE_CATEGORY}")
    else:
        await update.message.reply_text(f"Language selected: English.\nFree category: {FREE_CATEGORY}")
    await send_category_prompt(update, context)

async def send_category_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user_premium.get(user.id, False):
        text = "Elige una categoría para comenzar tu chat premium:\n" + "\n".join(f"- {c}" for c in CATEGORIES)
    else:
        text = f"Solo tienes acceso a la categoría gratuita: {FREE_CATEGORY}\nPara más, suscríbete premium."
    await update.message.reply_text(text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    lang = context.user_data.get('language', 'english')
    is_premium = user_premium.get(user.id, False)
# Si usuario no premium y quiere categoria paga
    if text in CATEGORIES and not is_premium:
        await update.message.reply_text("Esta categoría es premium. Por favor, suscríbete para acceder.")
        return
    elif text not in CATEGORIES and text != FREE_CATEGORY:
        await update.message.reply_text("Por favor, elige una categoría válida o usa la categoría gratuita.")
        return

    # Aquí llamarías a OpenAI para responder con personalidad según categoría y lenguaje
    prompt = f"Usuario habla en {lang}. Categoría: {text}. Responde de manera flirty, dominante y juguetona."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = "Lo siento, hubo un error con la IA. Intenta más tarde."

    await update.message.reply_text(reply)

if name == "main":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), language_choice))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()