
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

ADMIN_BOT_TOKEN = "YOUR_ADMIN_BOT_TOKEN"

async def forward_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and "/done" in update.message.text:
        try:
            tg_id = int(update.message.text.split()[1])
            await context.bot.send_message(
                chat_id=tg_id,
                text="🎁 Алмазы отправлены! Спасибо за покупку!"

/Rate — чтобы оценить наш бот"
            )
        except:
            await update.message.reply_text("❌ Ошибка. Используй так: /done telegram_id")

if __name__ == "__main__":
    app = ApplicationBuilder().token(ADMIN_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, forward_command))
    print("Admin bot is running...")
    app.run_polling()
