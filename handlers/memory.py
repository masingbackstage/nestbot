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

    lines = ["Moje wspomnienia o Tobie:\n"]
    for i, m in enumerate(memories, 1):
        lines.append(f"{i}. [{m.memory_type}] {m.content}")

    text = "\n".join(lines)

    for i in range(0, len(text), 4000):
        await update.message.reply_text(text[i:i+4000])


@require_authorized
async def handle_forget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Tej funkcji jeszcze nie ma — napisz do admina jeśli chcesz usunąć wspomnienia."
    )
