import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers import handle_message, handle_start, handle_pdf, handle_photo
from handlers import handle_forget, handle_memories
from services import ChatService, DocumentService
from config import settings
from db.postgres import SessionLocal

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=settings.log_level,
)
logger = logging.getLogger(__name__)


def main() -> None:
    db = SessionLocal()

    app = ApplicationBuilder().token(settings.telegram_bot_token).build()

    app.bot_data["chat_service"] = ChatService(db)
    app.bot_data["document_service"] = DocumentService(db)

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("memories", handle_memories))
    app.add_handler(CommandHandler("forget", handle_forget))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    logger.info(f"Bot starting (env={settings.app_env}, model={settings.llm_model})")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
