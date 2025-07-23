import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Получаем переменные из окружения
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
print("Admin bot token loaded")
async def forward_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and update.message.text.startswith("/done"):
        parts = update.message.text.split()
        if len(parts) == 2 and parts[1].isdigit():
            tg_id = int(parts[1])
            try:
                await context.bot.send_message(
                    chat_id=tg_id,
                    text="🎁 Алмазы успешно отправлены! Спасибо за покупку!\n\n/Rate - чтобы оценить наш бот"
                )
                await update.message.reply_text("✅ Клиенту отправлено сообщение.")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка отправки: {e}")
        else:
            await update.message.reply_text("❗ Используй команду так: /done <Telegram_ID>")
    else:
        await update.message.reply_text("🤖 Я жду команду вида: /done <Telegram_ID>")

if __name__ == "__main__":
    app = ApplicationBuilder().token(ADMIN_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_command))
    app.add_handler(MessageHandler(filters.COMMAND, forward_command))
    print("Admin bot is running...")
    app.run_polling()
