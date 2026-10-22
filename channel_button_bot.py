import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
APP_URL = "https://rosalynx.github.io/tarot-mini-app/"

logging.basicConfig(level=logging.INFO)

async def add_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post

    if not post or str(post.chat.id) != CHANNEL_ID:
        return

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "🍀 Мне повезёт",
            web_app=WebAppInfo(url=APP_URL)
        )
    ]])

    try:
        await context.bot.edit_message_reply_markup(
            chat_id=post.chat.id,
            message_id=post.message_id,
            reply_markup=keyboard
        )
    except Exception:
        logging.exception("Не удалось добавить кнопку")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, add_button))
    app.run_polling(
        allowed_updates=["channel_post"]
    )

if __name__ == "__main__":
    main()
