from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

users = {}

def intro(bot, update):
    update.message.reply_text("Hallo")
    update.message.reply_text("Ich bin <epischer botname>.")
    update.message.reply_text("Wie lautet dein Name?")
    return GETNAME

def set_name(bot, update):
    users[update.message.chat_id] = {
        "name" : update.message.text
    }
    update.message.reply_text("Freut mich "+update.message.text)
    return UNFINISHED

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

UNFINISHED, GETNAME = range(2)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', intro)],
    states = {
        GETNAME: [MessageHandler(Filters.text, set_name)],
        UNFINISHED: [MessageHandler(Filters.text, echo)]
    },
    fallbacks = [CommandHandler('reset', intro)]

)
