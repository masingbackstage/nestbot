import logging

from telegram import Update
from telegram.ext import ContextTypes

from middleware import require_authorized

logger = logging.getLogger(__name__)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Cześć!\n"
        "/memories — lista moich wspomnień o Tobie\n"
        "/forget — usuń wszystkie wspomnienia"
    )


@require_authorized
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    query = update.message.text

    await update.message.chat.send_action("typing")

    svc = context.bot_data["chat_service"]

    response = await svc.respond(
        telegram_id=str(user.id),
        display_name=user.full_name,
        query=query,
    )

    await update.message.reply_text(response)
