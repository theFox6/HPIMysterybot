from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from threading import Timer
import users

GETNAME, START, QUEST5, QUEST1, QUEST2, QUEST3, QUEST4, UNFINISHED = range(8)

def intro(bot, update):
    update.message.reply_text("Hallo, ich brauche deine Hilfe! Ich wurde gefangen genommen und muss entkommen!") 
    update.message.reply_text("Ich bin Calliope.")
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

def quest5(bot, update):
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open('drei_türen.jpg', 'rb'))
    reply_markup = ReplyKeyboardMarkup([['1'],['2'],['3']], one_time_keyboard=True)
    bot.send_message(chat_id=chat_id, text="Welche Tür soll ich nehmen?", reply_markup=reply_markup)
    return QUEST5
'''
def answer1(bot, update):
    answer = update.message.text
    if answer == '1':
        reply_markup = ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Das war die richtige Tür.", reply_markup=reply_markup)
        update.message.reply_text("Danke. Ich weiß nicht, ob ich ohne dich noch leben würde.")
        return quest2(bot, update)
    else:
        reply_markup = ReplyKeyboardMarkup([['neu anfangen']], one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, 
                  text="Du hast mich getötet, ich verbrenne!!!",
                  reply_markup=reply_markup)
        return START
'''
def quest6(bot, update):
    update.message.reply_text("Nun musst du mir noch bei diesem Rätsel helfen! Ich kann ihn sonst nicht befreien.")
    update.message.reply_text("Es lautet: Was kannst du sehen, aber nicht nehmen?\nEin Tipp wurde beigelegt: Du bist der Grund!")
    return QUEST6

def answer6(bot, update):
    answer = update.message.text
    if answer == "schatten" or answer == "Schatten":
        update.message.reply_text("Richtig, danke für die Hilfe ma boy! Ich konnte ihn befreien! \nDanke für deine hilfe!")
        return quest3(bot, update)
    else:
        update.message.reply_text("Oh nein, du hast mich getötet!")
        update.message.reply_text("versuchs doch nochmal")
    
def quest7(bot, update):
    update.message.reply_text("Nun musst du mir noch bei diesem Rätsel helfen! Ich kann ihn sonst nicht befreien.")
    update.message.reply_text("Dort hängt es an der Wand, das gibt mir jeden morgen die Hand.")
    t = Timer(10, tipp3, args=[bot, update])
    u = users.all[update.message.chat_id]
    print("registering timer")
    u['tippTimer'] = t
    print("starting timer")
    t.start()
    print("next state")
    return QUEST3

def tipp3(bot, update):
    print("tipp geben")
    users.all[update.message.chat_id]['tippAngeboten'] = True
    reply_markup = ReplyKeyboardMarkup([['Tipp'],['Noch nicht.']], one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, 
        text="Brauchst du einen Tipp?",
        reply_markup=reply_markup)

def answer3(bot, update):
    answer = update.message.text
    user = users.all[update.message.chat_id]
    print(answer)
    if user['tippAngeboten'] and answer == "Tipp":
        user['tippAngeboten'] = False
        reply_markup = ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Der Gegenstand befindet sich im Badezimmer.", reply_markup=reply_markup)
    elif user['tippAngeboten'] and answer == "Noch nicht.":
        update.message.reply_text('OK, du kannst ihn mit "Tipp" später noch bekommen.')
    elif answer == "Handtuch" or answer == "handtuch":
        user['tippAngeboten'] = False
        user['tippTimer'].cancel()
        update.message.reply_text("Sehr gut, du bist ein schlaues Ding.")
        return quest4(bot, update)
    else:
        update.message.reply_text("Oh nein, du hast mich getötet!")
        update.message.reply_text("versuchs doch nochmal")
    

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
        update.message.reply_text("Oh nein, " + users.all[update.message.chat_id].name + " du hast mich getötet!")
        update.message.reply_text("versuchs doch nochmal")
    

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', intro)],
    states = {
        GETNAME: [MessageHandler(Filters.text, set_name)],
        START: [MessageHandler(Filters.text, quest1)],
        QUEST5: [MessageHandler(Filters.text, quest6, quest7, quest8)],
        QUEST6: [MessageHandler(Filters.text, answer6)],
        QUEST3: [MessageHandler(Filters.text, answer3)],
        QUEST4: [MessageHandler(Filters.text, answer4)],
        UNFINISHED: [MessageHandler(Filters.text, echo)]
    },
    fallbacks = [CommandHandler('reset', intro)]
)
