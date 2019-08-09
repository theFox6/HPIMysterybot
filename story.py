from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, Location
from threading import Timer
import users, hints, math

GETNAME, START, QUEST1, QUEST5, QUEST6, QUEST7, QUEST8, UNFINISHED = range(8)

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

def quest1(bot, update):
    location_keyboard = KeyboardButton(text="Ich bin angekommen.", request_location=True)
    reply_markup = ReplyKeyboardMarkup([[location_keyboard]])
    bot.send_message(chat_id=update.message.chat_id, 
                 text="Baum", 
                  reply_markup=reply_markup)
    return QUEST1

def measure(lat1, lon1, lat2, lon2):
    R = 6378.137 # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000; # meters

def answer1(bot, update):
    location = update.message.location
    diff = measure(location.latitude, location.longitude, 52.394, 13.133)
    if diff<20:
        reply_markup = ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text='Du bist da.', reply_markup=reply_markup)
        return quest5(bot, update)
    else:
        update.message.reply_text("Du musst noch "+ str(round(diff)) + " Meter gehen.")

def quest5(bot, update):
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open('drei_tueren.jpg', 'rb'))
    reply_markup = ReplyKeyboardMarkup([['1'],['2'],['3']], one_time_keyboard=True)
    bot.send_message(chat_id=chat_id, text="Welche Tür soll ich nehmen?", reply_markup=reply_markup)
    return QUEST5

def whichquest(bot, update):
    answer = update.message.text
    try:
        answer = int(answer)
    except ValueError:
        update.message.reply_text("Das ist keine Zahl!")
        return
    if answer<1 or answer>3:
        update.message.reply_text("Das steht auf keiner Tür!")
        return
    reply_markup = ReplyKeyboardRemove()
    bot.send_message(chat_id=update.message.chat_id, text='OK, ich nehme tür ' + str(answer), reply_markup=reply_markup)
    if answer == 1:
        return quest6(bot,update)
    elif answer == 2:
        return quest7(bot, update)
    elif answer == 3:
        return quest8(bot, update)

def quest6(bot, update):
    update.message.reply_text("Nun musst du mir noch bei diesem Rätsel helfen! Ich kann ihn sonst nicht befreien.")
    update.message.reply_text("Es lautet: Was kannst du sehen, aber nicht nehmen?\nEin Tipp wurde beigelegt: Du bist der Grund!")
    return QUEST6

def answer6(bot, update):
    answer = update.message.text
    if answer == "schatten" or answer == "Schatten":
        update.message.reply_text("Richtig, danke für die Hilfe ma boy! Ich konnte ihn befreien!")
        return quest3(bot, update)
    else:
        update.message.reply_text("Oh nein, du hast mich getötet!")
        update.message.reply_text("versuchs doch nochmal")
    
def quest7(bot, update):
    update.message.reply_text("Nun musst du mir noch bei diesem Rätsel helfen! Ich kann ihn sonst nicht befreien.")
    update.message.reply_text("Dort hängt es an der Wand, das gibt mir jeden morgen die Hand.")
    print("run hint timer")
    hints.run_timer(bot, update.message.chat_id, 10, "Brauchst du einen Tipp?")
    print("switch state")
    return QUEST7

def answer7(bot, update):
    answer = update.message.text
    if hints.handle_hint(bot, update.message.chat_id, answer, "Der Gegenstand befindet sich im Badezimmer."):
        return
    elif answer == "Handtuch" or answer == "handtuch":
        hints.cancel(update.message.chat_id)
        update.message.reply_text("Richtig, danke für die Hilfe ma boy! Ich konnte ihn befreien!")
        return quest4(bot, update)
    else:
        update.message.reply_text("Oh nein, du hast mich getötet!")
        update.message.reply_text("versuchs doch nochmal")
    

def quest8(bot,update):
    update.message.reply_text("Nun musst du mir noch bei diesem Rätsel helfen! Ich kann ihn sonst nicht befreien.")
    update.message.reply_text("wer es macht, der sagt es nicht,\nwer es nimmt, der kennt es nicht,\nwer es kennt, der nimmt es nicht.")
    '''sleep(10000)
    update.message.text("Brauchst du einen Tipp?")
    answer = update.message.text
    if answer == "ja":
        update.message.text("Es hat etwas mit geld zu tun")'''
    return QUEST8
    
def answer8(bot, update):
    answer = update.message.text
    if answer == "Falschgeld" or answer == "falschgeld" or answer == "Blüten" or answer == "blüten" or answer == "Blüte" or answer == "blüte" or answer == "Gift" or answer == "gift":
        update.message.reply_text("Richtig, danke für die Hilfe ma boy! Ich konnte ihn befreien!")
        return UNFINISHED
    else:
        update.message.reply_text("Oh nein, " + users.all[update.message.chat_id]['name'] + " du hast mich getötet!")
        update.message.reply_text("versuchs doch nochmal")
    

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', intro)],
    states = {
        GETNAME: [MessageHandler(Filters.text, set_name)],
        START: [MessageHandler(Filters.text, quest1)],
        QUEST1: [MessageHandler(Filters.location, answer1)],
        QUEST5: [MessageHandler(Filters.text, whichquest)],
        QUEST6: [MessageHandler(Filters.text, answer6)],
        QUEST7: [MessageHandler(Filters.text, answer7)],
        QUEST8: [MessageHandler(Filters.text, answer8)],
        UNFINISHED: [MessageHandler(Filters.text, echo)]
    },
    fallbacks = [CommandHandler('reset', intro)]
)
