from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from threading import Timer

def give_hint(bot, chat_id, message):
    users.all[chat_id]['offeredHint'] = True
    reply_markup = ReplyKeyboardMarkup([['Tipp'],['Noch nicht.']], one_time_keyboard=True)
    bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)

def run_timer(bot, chat_id, time, message):
    t = Timer(time, give_hint, args=[bot, chat_id, message])
    u = users.all[chat_id]['hintTimer'] = t
    t.start()

def handle_hint(bot, chat_id, hint_text):
    user = users.all[chat_id]
    if user['offeredHint'] and answer == "Tipp":
        user['offeredHint'] = False
        # TODO make removal optional
        reply_markup = ReplyKeyboardRemove()
        bot.send_message(chat_id=chat_id, text=hint_text, reply_markup=reply_markup)
        return True
    elif user['tippAngeboten'] and answer == "Noch nicht.":
        bot.send_message(chat_id = chat_id, text = 'OK, du kannst ihn mit "Tipp" später noch bekommen.')
        return True
    else:
        return False
