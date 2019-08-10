from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, Location, ChatAction
from threading import Timer
import users, hints, math, logging

GETNAME, START, QUEST1, QUEST2, QUEST3, QUEST4, QUEST5, QUEST6, QUEST7, QUEST8, THEEND = range(11)

def intro(bot, update):
    update.message.reply_text("Hallo, ich brauche deine Hilfe! Ich wurde gefangen genommen und du must mich befreien, indem du verschiedene Rätsel löst.") 
    update.message.reply_text("Ich bin Calliope.")
    update.message.reply_text("Wie lautet dein Name?")
    return GETNAME
    
def set_name(bot, update):
    name = update.message.text
    chatId = update.message.chat_id
    users.create(chatId, name)
    reply_markup = ReplyKeyboardMarkup([['los gehts']], one_time_keyboard=True)
    bot.send_message(chat_id=chatId, text="Freut mich " + name, reply_markup=reply_markup)
    return START

def quest1(bot, update):
    users.start_time(update.message.chat_id)
    logging.info("building location keyboard")
    location_keyboard = KeyboardButton(text="Ich bin angekommen.", request_location=True)
    logging.info("building reply keyboard markup")
    reply_markup = ReplyKeyboardMarkup([[location_keyboard]])
    logging.info("sending message")
    bot.send_message(chat_id=update.message.chat_id, 
                 text="Finde den bekanntesten Baum auf dem Gelände", 
                  reply_markup=reply_markup)
    logging.info("changing state")
    return QUEST1

def measure(lat1, lon1, lat2, lon2):
    R = 6378.137 # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000 # meters

def answer1(bot, update):
    location = update.message.location
    diff = measure(location.latitude, location.longitude, 52.394, 13.133)
    if diff<30:
        reply_markup = ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text='Du bist am Startpunkt angekommen.', reply_markup=reply_markup)
        return quest2(bot, update)
    else:
        update.message.reply_text("Du musst noch "+ str(round(diff)) + " Meter gehen.")

def quest2(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
    bot.send_photo(chat_id=chat_id, photo=open('Kunstwerk.jpg', 'rb'))
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text("Bitte identifiziere dieses Kunstwerk für mich, indem du mir den Namen nennst.")
    return QUEST2

def answer2(bot, update):
    answer = update.message.text.lower()
    if answer == "kapuzinerkresse blau":
        update.message.reply_text("Perfekt, das hast du gut gemacht!")
        return quest3(bot, update)
    else:
        update.message.reply_text("Versuchs doch nochmal.")

def quest3(bot, update):
    chat_id = update.message.chat_id
    update.message.reply_text("Finde bitte für mich den Ort, wo das Schaf seine Batterien aufläd.")
    #reply_markup = ReplyKeyboardMarkup([['1','2','3'],['4','5','6'],['7','8','9'],['0']])
    bot.send_message(chat_id=chat_id, text="Ich benötige die Inventarnummer die darauf steht, als code um eine Tür zu öffnen")
    return QUEST3

def answer3(bot, update):
    answer = update.message.text
    if answer == "007668":
        update.message.reply_text("Du bist ein Held, bald bin ich durch dich frei!")
        return quest4(bot, update)
    else:
        update.message.reply_text("Versuchs doch nochmal.")


def quest4(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_AUDIO)
    bot.send_audio(chat_id=update.message.chat_id, audio=open('mystery_sound.mp3', 'rb'))
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_text("Was bewacht diesen Ort?")
    return QUEST4

def answer4(bot, update):
    answer = update.message.text.lower()
    if answer == "figur" or answer == "statue" or answer == "person" or answer == "mann" or answer == "mr. net" or answer == "mr net":
        update.message.reply_text("Uh nice, das bringt uns fast ans Ziel! Nur noch eine weitere Quest.")
        return quest5(bot, update)
    else:
        update.message.reply_text("Oh nein, du hast mich getötet!")
        update.message.reply_text("versuchs doch nochmal.")

def quest5(bot, update):
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open('drei_tueren.jpg', 'rb'))
    reply_markup = ReplyKeyboardMarkup([['1'],['2'],['3']], one_time_keyboard=True)
    bot.send_message(chat_id=chat_id, text="Triff nun eine Kluge entscheidung. Welche Tür wählst du?", reply_markup=reply_markup)
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

def hint6(bot, chat_id):
    hints.run_timer(bot, chat_id, "Es folgt dir auf Schritt und Tritt.",
        time = 120, offer_text = "Ich habe auch noch einen besseren Tipp.")

def quest6(bot, update):
    update.message.reply_text("Nun musst du noch dieses Rätsel für mich lösen! Dann bin ich frei!")
    update.message.reply_text("Es lautet: Was kannst du sehen, aber nicht nehmen?\nEin Tipp wurde beigelegt: Du bist der Grund!")
    hints.run_timer(bot, update.message.chat_id, "Ohne Licht existiert es nicht.", func = hint6)
    return QUEST6

def answer6(bot, update):
    answer = update.message.text.lower()
    if answer == "schatten":
        update.message.reply_text("Richtig, danke für die Hilfe ma boy! Endlich bin ich dank dir frei!")
        return theEnd(bot, update)
    else:
        update.message.reply_text("Oh nein, du hast mich getötet!")
        update.message.reply_text("versuchs doch nochmal")
    
def quest7(bot, update):
    update.message.reply_text("Nun musst du noch dieses Rätsel für mich lösen! Dann bin ich frei!")
    update.message.reply_text("Dort hängt es an der Wand, das gibt mir jeden morgen die Hand.")
    logging.info("run hint timer")
    hints.run_timer(bot, update.message.chat_id, "Der Gegenstand befindet sich im Badezimmer.")
    logging.info("switch state")
    return QUEST7

def answer7(bot, update):
    answer = update.message.text.lower()
    if answer == "handtuch" or answer == "türklinke":
        hints.cancel(update.message.chat_id)
        update.message.reply_text("Richtig, danke für die Hilfe ma boy! Endlich bin ich dank dir frei!")
        return theEnd(bot, update)
    else:
        update.message.reply_text("Oh nein, du hast mich getötet!")
        update.message.reply_text("versuchs doch nochmal")
    

def quest8(bot,update):
    update.message.reply_text("Nun musst du noch dieses Rätsel für mich lösen! Dann bin ich frei!")
    update.message.reply_text("wer es macht, der sagt es nicht,\nwer es nimmt, der kennt es nicht,\nwer es kennt, der nimmt es nicht.")
    hints.run_timer(bot, update.message.chat_id, "Es hat etwas mit geld zu tun")
    return QUEST8
    
def answer8(bot, update):
    answer = update.message.text.lower()
    if answer == "falschgeld" or answer == "blüten" or answer == "blüte" or answer == "gift":
        hints.cancel(update.message.chat_id)
        update.message.reply_text("Richtig, danke für die Hilfe ma boy! Endlich bin ich dank dir frei!")
        return theEnd(bot, update)
    else:
        update.message.reply_text("Oh nein, " + users.all[update.message.chat_id]['name'] + " du hast mich getötet!")
        update.message.reply_text("versuchs doch nochmal")
    

def theEnd(bot, update):
    chatId = update.message.chat_id
    name = users.all[chatId]['name']
    reply_markup = ReplyKeyboardMarkup([['noch einmal spielen'],['highscores zeigen']], one_time_keyboard=True)
    bot.send_message(chat_id=chatId, text="Glückwunsch " + name + " du hast das Spiel geschafft.", reply_markup=reply_markup)
    bot.sendSticker(chatId, bot.get_sticker_set("MabelsStickers").stickers[2])
    users.end_time(bot,chatId)
    return THEEND

def restart(bot, update):
    if update.message.text == "noch einmal spielen":
        reply_markup = ReplyKeyboardRemove()
        bot.send_message(chat_id=update.message.chat_id, text="Dann noch einmal.", reply_markup=reply_markup)
        return intro(bot, update)
    if update.message.text == "highscores zeigen":
        scores = ""
        for score in users.highscores:
            scores += score.name + ': ' + str(score.time)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', intro)],
    states = {
        GETNAME: [MessageHandler(Filters.text, set_name)],
        START:  [MessageHandler(Filters.text, quest1)],
        QUEST1: [MessageHandler(Filters.location, answer1)],
        QUEST2: [MessageHandler(Filters.text, answer2)],
        QUEST3: [MessageHandler(Filters.text, answer3)],
        QUEST4: [MessageHandler(Filters.text, answer4)],
        QUEST5: [MessageHandler(Filters.text, whichquest)],
        QUEST6: [MessageHandler(Filters.text, answer6)],
        QUEST7: [MessageHandler(Filters.text, answer7)],
        QUEST8: [MessageHandler(Filters.text, answer8)],
        THEEND: [MessageHandler(Filters.text, restart)]
    },
    fallbacks = [CommandHandler('reset', intro)]
)
