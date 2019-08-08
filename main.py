from telegram.ext import Updater, CommandHandler, Filters, ConversationHandler, MessageHandler

with open("token.txt") as token_file:
    token = token_file.read().strip()

NEUTRAL, WAITING = range(2)

def machSchrott(bot, update):
    update.message.reply_text("Schrott")
    return NEUTRAL

def start_timer(bot, update):
    update.message.reply_text("geht ned")

def delete_timer(bot, update):
    update.message.reply_text("nope")

def stop_timer(bot, update):
    update.message.reply_text("unimplemented")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def sleep(bot, update):
    echo(bot, update)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', machSchrott)],
    states = {
        NEUTRAL: [CommandHandler('new',start_timer), MessageHandler(Filters.text, echo)],
        WAITING: [CommandHandler('off', stop_timer), MessageHandler(Filters.text, sleep)]
    },
    fallbacks = [CommandHandler('done', delete_timer)]

)

def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
