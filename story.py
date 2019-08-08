from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import users

GETNAME, START, QUEST1, QUEST1, QUEST2, QUEST3, QUEST4, UNFINISHED = range(8)

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
        return quest2(bot, update)
    else:
        reply_markup = ReplyKeyboardMarkup([['neu anfangen']], one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, 
                  text="Du hast mich getötet, ich verbrenne!!!",
                  reply_markup=reply_markup)
        return START

def quest2(bot, update):
    update.message.reply_text("Ich muss ein weiteres Rätsel beantworten. Bitte hilft mir ich weiß es nicht.")
    update.message.reply_text("Was kannst du sehen, aber nicht nehmen?\nEin Tipp wurde beigelegt: Du bist der Grund!")
    return QUEST2

def answer2(bot, update):
    answer = update.message.text
    if answer == "schatten" or answer == "Schatten":
        update.message.reply_text("Richtig, danke für die Hilfe ma boy!")
        return quest3(bot, update)
    else:
        update.message.reply_text("Oh nein, du hast mich getötet!")
    
def quest3(bot, update):
    update.message.reply_text("Jo, ich hab noch eins!")
    update.message.reply_text("Dort hängt es an der Wand, das gibt mir jeden morgen die Hand.")
    '''sleep(10000)
    update.message.text("Brauchst du einen Tipp?")
    answer = update.message.text
    if answer == "ja":
        update.message.text("Der Gegenstand befindet sich im Badezimmer.")'''
    return QUEST3

def answer3(bot, update):
    answer = update.message.text
    if answer == "Handtuch" or answer == "handtuch":
        update.message.reply_text("Sehr gut, du bist ein schlaues Ding.")
        return quest4(bot, update)
    else:
        update.message.reply_text("Oh nein, du hast mich getöt!")
    

def quest4(bot,update):
    update.message.reply_text("Ich bin immernoch gefangen und ich stehe vor einem weiteren Rätsel wofür ich deine Hilfe benötige. Es ist echt schwer.")
    update.message.reply_text("wer es macht, der sagt es nicht,\nwer es nimmt, der kennt es nicht,\nwer es kennt, der nimmt es nicht.")
    '''sleep(10000)
    update.message.text("Brauchst du einen Tipp?")
    answer = update.message.text
    if answer == "ja":
        update.message.text("Es hat etwas mit geld zu tun")'''
    return QUEST4
    
def answer4(bot, update):
    answer = update.message.text
    if answer == "Falschgeld" or answer == "falschgeld" or answer == "Blüten" or answer == "blüten" or answer == "Blüte" or answer == "blüte" or answer == "Spielgeld" or answer == "spielgeld":
        update.message.reply_text("Bravo, das rätsel war etwas knifflig")
        return UNFINISHED
    else:
        update.message.reply_text("Oh nein, du hast mich getöt!")
    

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', intro)],
    states = {
        GETNAME: [MessageHandler(Filters.text, set_name)],
        START: [MessageHandler(Filters.text, quest1)],
        QUEST1: [MessageHandler(Filters.text, answer1)],
        QUEST2: [MessageHandler(Filters.text, answer2)],
        QUEST3: [MessageHandler(Filters.text, answer3)],
        QUEST4: [MessageHandler(Filters.text, answer4)],
        UNFINISHED: [MessageHandler(Filters.text, echo)]
    },
    fallbacks = [CommandHandler('reset', intro)]

)
