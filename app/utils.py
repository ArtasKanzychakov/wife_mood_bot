# app/utils.py

from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps

def send_typing_action(func):
    @wraps(func)
    async def command_func(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if update.message:
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action="typing")
        elif update.callback_query:
            await context.bot.send_chat_action(chat_id=update.callback_query.message.chat_id, action="typing")
        return await func(update, context, *args, **kwargs)
    return command_func
