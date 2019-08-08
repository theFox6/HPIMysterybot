from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters

users = {}

def intro(bot, update):
    update.message.reply_text("Hallo, ich brauche deine Hilfe! Ich wurde gefangen genommen und muss entkommen!") 
    update.message.reply_text("Ich bin Caliope.")
    update.message.reply_text("Wie lautet dein Name?")
    return GETNAME

def set_name(bot, update):
    users[update.message.chat_id] = {
        "name" : update.message.text
    }
    update.message.reply_text("Freut mich "+update.message.text)
    return UNFINISHED

def quest1(bot, update)
    bot.send_photo(chat_id=update.message.chat_id, photo=open('3_tueren_quest.jpg', 'rb'))
    update.message.reply_text("Welche Tür soll ich nehmen?")
    return QUEST1

def answer1(bot, update):
    answer = update.message.text
    if answer == 1
        update.message.reply_text("Das war die richtige Tür.")
        update.message.reply_text("Danke, ich weiss nicht ob ich ohne dich noch leben würde.")
        return 
    else
        update.message.reply_text("Du hast mich getötet, ich verbrenne!!!")
        return GETNAME

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

UNFINISHED, GETNAME, QUEST1 = range(3)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', intro)],
    states = {
        GETNAME: [MessageHandler(Filters.text, set_name)],
        UNFINISHED: [MessageHandler(Filters.text, quest1)],
        QUEST1: [MessageHandler(Filters.text, answer1)]
    },
    fallbacks = [CommandHandler('reset', intro)]

)
