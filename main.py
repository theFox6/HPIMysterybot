from telegram.ext import Updater, CommandHandler, Filters, ConversationHandler, MessageHandler

with open("token.txt") as token_file:
    token = token_file.read().strip()

users = {}

UNFINISHED, GETNAME = range(2)

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

'''
def start_timer(bot, update):
    update.message.reply_text("geht ned")

def delete_timer(bot, update):
    update.message.reply_text("nope")

def stop_timer(bot, update):
    update.message.reply_text("unimplemented")

def sleep(bot, update):
    echo(bot, update)
'''

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', intro)],
    states = {
        GETNAME: [MessageHandler(Filters.text, set_name)],
        UNFINISHED: [MessageHandler(Filters.text, echo)]
    },
    fallbacks = [CommandHandler('reset', intro)]

)

def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    print("bot ready")
    updater.idle()

if __name__ == '__main__':
    main()
