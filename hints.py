from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle
from telegram.ext import CallbackQueryHandler
from threading import Timer
import logging,users

def give_hint(bot, chat_id, hint_text):
    users.all[chat_id]['offeredHint'] = hint_text
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Tipp",callback_data="Tipp")]])
    bot.send_message(chat_id=chat_id, text="Brauchst du einen Tipp?", reply_markup=reply_markup)

def run_timer(bot, chat_id, time, hint_text):
    logging.debug("creating hint timer")
    t = Timer(time, give_hint, args=[bot, chat_id, hint_text])
    logging.info("registering timer")
    users.all[chat_id]['hintTimer'] = t
    logging.info("starting timer")
    t.start()

def handle_hint(bot, update):
    user = users.all[update.effective_message.chat_id]
    if not user['offeredHint']:
        return
    bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text=user['offeredHint'])
    #bot.send_message(chat_id=update.effective_message.chat_id, text=user['offeredHint'])
    #user['offeredHint'] = False

def cancel(chat_id):
    user = users.all[chat_id]
    user['offeredHint'] = False
    user['hintTimer'].cancel()

callback_handler = CallbackQueryHandler(handle_hint, pattern="Tipp")
