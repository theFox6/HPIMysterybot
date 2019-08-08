from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import users

GETNAME, START, QUEST1, UNFINISHED = range(4)

def intro(bot, update):
    update.message.reply_text("Hallo, ich brauche deine Hilfe! Ich wurde gefangen genommen und muss entkommen!") 
    update.message.reply_text("Ich bin Caliope.")
    update.message.reply_text("Wie lautet dein Name?")
    return GETNAME

def set_name(bot, update):
    name = update.message.text
    chatId = update.message.chat_id
    users.create(chatId, name)
    reply_markup = ReplyKeyboardMarkup([['los gehts']], one_time_keyboard=True)
    bot.send_message(chat_id=chatId, text="Freut mich " + name, 
                  reply_markup=reply_markup)
    return START

def quest1(bot, update):
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open('3_tueren_quest.jpg', 'rb'))
    reply_markup = ReplyKeyboardMarkup([['1'],['2'],['3']], one_time_keyboard=True)
    bot.send_message(chat_id=chat_id, 
                  text="Welche Tür soll ich nehmen?",
                  reply_markup=reply_markup)
    return QUEST1

def answer1(bot, update):
    answer = update.message.text
    if answer == '1':
        update.message.reply_text("Das war die richtige Tür.")
        update.message.reply_text("Danke, ich weiss nicht ob ich ohne dich noch leben würde.")
        return UNFINISHED
    else:
        reply_markup = ReplyKeyboardMarkup([['neu anfangen']], one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, 
                  text="Du hast mich getötet, ich verbrenne!!!",
                  reply_markup=reply_markup)
        return START

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', intro)],
    states = {
        GETNAME: [MessageHandler(Filters.text, set_name)],
        START: [MessageHandler(Filters.text, quest1)],
        QUEST1: [MessageHandler(Filters.text, answer1)],
        UNFINISHED: [MessageHandler(Filters.text, echo)]
    },
    fallbacks = [CommandHandler('reset', intro)]

)
