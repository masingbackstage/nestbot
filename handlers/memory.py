import logging

from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

from middleware import require_authorized

logger = logging.getLogger(__name__)


@require_authorized
async def handle_memories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    svc = context.bot_data["chat_service"]
    memories = svc.list_memories(telegram_id=str(update.effective_user.id))

    if not memories:
        await update.message.reply_text("Nie mam jeszcze żadnych wspomnień o Tobie.")
        return

    lines = ["*Moje wspomnienia o Tobie:*\n"]
    for i, m in enumerate(memories[:20], 1):
        content = escape_markdown(m.content, version=2)
        lines.append(f"{i}\\. {content}")

    await update.message.reply_text("\n".join(lines), parse_mode="MarkdownV2")


@require_authorized
async def handle_forget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Tej funkcji jeszcze nie ma — napisz do admina jeśli chcesz usunąć wspomnienia."
    )
