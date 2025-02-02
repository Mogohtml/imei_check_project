import pytest
from app.bot import handle_message
from telegram import Update, Message
from telegram.ext import CallbackContext

def test_handle_message():
    update = Update(123456789)
    update.message = Message(123456789, 123456789, "123456789012345")
    context = CallbackContext(None)
    handle_message(update, context)
    assert update.message.reply_text.called
