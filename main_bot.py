
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

MAIN_BOT_TOKEN = "YOUR_MAIN_BOT_TOKEN"
ADMIN_BOT_ID = YOUR_ADMIN_BOT_ID  # int, not string
RATING_CHANNEL = "@your_channel"

user_ff_ids = {}
user_states = {}

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Введи свой Free Fire ID:")
    user_states[update.effective_user.id] = "WAITING_FF_ID"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_states.get(user_id)

    if state == "WAITING_FF_ID":
        ff_id = update.message.text
        user_ff_ids[user_id] = ff_id
        user_states[user_id] = "WAITING_PAYMENT"
        await update.message.reply_text("✅ Отлично! Теперь оплати и пришли скрин оплаты 💵")
    elif state == "WAITING_PAYMENT" and update.message.photo:
        ff_id = user_ff_ids.get(user_id, "Неизвестен")
        caption = f"💰 Новая оплата!
FF ID: {ff_id}
Telegram: @{update.effective_user.username or 'нет'}"
        photo = update.message.photo[-1]
        await context.bot.send_photo(
            chat_id=ADMIN_BOT_ID,
            photo=photo.file_id,
            caption=caption
        )
        await update.message.reply_text("📤 Скрин отправлен! Ждите подтверждения от продавца.")
    else:
        await update.message.reply_text("⛔ Пожалуйста, следуйте инструкции.")

async def send_rating_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("⭐️" * i, callback_data=str(i))] for i in range(1, 11)]
    await update.message.reply_text(
        "🎉 Спасибо за покупку! Оцени наш бот от 1 до 10:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    rating = query.data
    user = query.from_user
    text = f"⭐️ Оценка от @{user.username or user.id}: {rating}/10"
    await context.bot.send_message(chat_id=RATING_CHANNEL, text=text)
    await query.edit_message_text("Спасибо за вашу оценку! ❤️")

if __name__ == "__main__":
    app = ApplicationBuilder().token(MAIN_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rate", send_rating_request))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))
    app.add_handler(CallbackQueryHandler(handle_rating))
    print("Main bot is running...")
    app.run_polling()
