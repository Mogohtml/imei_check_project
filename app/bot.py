import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from .utils import check_imei, is_user_allowed
from .config import TELEGRAM_BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    logger.info(f"Received message from user {user_id}")
    if not is_user_allowed(user_id):
        await update.message.reply_text("Вы не имеете доступа к этому боту.")
        logger.warning(f"Unauthorized access attempt from user {user_id}")
        return

    imei = update.message.text
    if not imei.isdigit() or len(imei) != 15:
        await update.message.reply_text("Неверный формат IMEI. IMEI должен содержать 15 цифр.")
        logger.warning(f"Invalid IMEI format from user {user_id}: {imei}")
        return

    try:
        result = check_imei(imei)
        await update.message.reply_text(f"Информация о IMEI: {result}")
        logger.info(f"Successfully processed IMEI {imei} for user {user_id}")
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при проверке IMEI. Пожалуйста, попробуйте позже.")
        logger.error(f"Error processing IMEI {imei} for user {user_id}: {e}")

async def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.start_polling()
    await application.idle()

if __name__ == '__main__':
    asyncio.run(main())
