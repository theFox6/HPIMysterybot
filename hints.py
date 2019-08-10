from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle
from telegram.ext import CallbackQueryHandler
from threading import Timer
import logging,users

def give_hint(bot, chat_id, hint_text, offer_text):
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Tipp",callback_data=hint_text)]])
    bot.send_message(chat_id=chat_id, text=offer_text, reply_markup=reply_markup)

def run_timer(bot, chat_id, hint_text, time = 60, func = False, offer_text = "Brauchst du einen Tipp?"):
    logging.debug("creating hint timer")
    t = Timer(time, give_hint, args=[bot, chat_id, hint_text, offer_text])
    logging.info("registering timer")
    users.all[chat_id]['hintTimer'] = t
    users.all[chat_id]['hintFunc'] = func
    logging.info("starting timer")
    t.start()

def handle_hint(bot, update):
    chat_id = update.effective_message.chat_id
    user = users.all[chat_id]
    bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=update.callback_query.data)
    if user['hintFunc']:
        user['hintFunc'](bot,chat_id)
    
def cancel(chat_id):
    user = users.all[chat_id]
    user['hintFunc'] = False
    user['hintTimer'].cancel()

callback_handler = CallbackQueryHandler(handle_hint)
