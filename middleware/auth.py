import logging
from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from config import settings

logger = logging.getLogger(__name__)


def require_authorized(func):
    @wraps(func)
    async def wrapper(
        update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs
    ):
        if not settings.allowed_telegram_ids:
            return await func(update, context, *args, **kwargs)

        user_id = update.effective_user.id
        if user_id not in settings.allowed_telegram_ids:
            logger.warning(
                f"Unauthorized access: {user_id} ({update.effective_user.full_name})"
            )
            await update.message.reply_text("Unauthorized access.")
            return

        return await func(update, context, *args, **kwargs)

    return wrapper
