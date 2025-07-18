import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re
import sys
sys.path.append('../AGI_Core/core')  # Добавляем путь к ядру (при локальной разработке)

from AGI_Core.core.agi_main import AGICore

MODEL_PATH = "/home/sukuna/.local/share/nomic.ai/GPT4All"
agi_core = AGICore(model_path=MODEL_PATH)

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ADMIN_TELEGRAM_ID = 5851852111  # Здесь твой ID
ALLOWED_USERS = {ADMIN_TELEGRAM_ID, 987654321}  # ID других разрешённых пользователей


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("Извините, у вас нет доступа.")
        return
    await update.message.reply_text("Привет! Я AGI интерфейс. Задайте вопрос.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("Извините, у вас нет доступа.")
        return

    prompt = update.message.text
    response = agi_core.generate_response(prompt)
    await update.message.reply_text(response)

def main():
    # Токен нужно положить в переменную окружения или прямо сюда
    TOKEN = "7659780236:AAH5SAXSDDsnonvXd0rureZ_Qm6-1oj7PZ8"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()

