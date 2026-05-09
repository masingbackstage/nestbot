import logging

from telegram import Update
from telegram.ext import ContextTypes

from middleware import require_authorized

logger = logging.getLogger(__name__)


@require_authorized
async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    doc = update.message.document
    if doc.mime_type != "application/pdf":
        return

    await update.message.reply_text("Przetwarzam PDF...")

    file = await doc.get_file()
    path = f"/tmp/{doc.file_name}"
    await file.download_to_drive(path)

    svc = context.bot_data["document_service"]
    chunks = svc.ingest_pdf(path=path, source=doc.file_name)
    saved = svc.save_chunks(
        external_ref=f"telegram:{update.effective_user.id}",
        display_name=update.effective_user.full_name,
        chunks=chunks,
        source=doc.file_name,
    )
    await update.message.reply_text(f"Zapisano {saved} fragmentów z PDF.")


@require_authorized
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Czytam zdjęcie...")

    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_bytes = bytes(await file.download_as_bytearray())

    svc = context.bot_data["document_service"]
    chunks = svc.ingest_image(image_bytes)
    saved = svc.save_chunks(
        external_ref=f"telegram:{update.effective_user.id}",
        display_name=update.effective_user.full_name,
        chunks=chunks,
        source=f"photo_{update.message.message_id}",
    )
    await update.message.reply_text(f"Zapisano {saved} fragmentów ze zdjęcia.")
