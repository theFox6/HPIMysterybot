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

def quest2(bot, update):
    update.message.reply_text("Ich muss ein weiteres Rätsel beantworten. Bitte hilft mir ich weiß es nicht.")
    update.message.reply_text("Was kannst du sehen, aber nicht nehmen? Ein Tipp wurde beigelegt: Du bist der Grund!")
    return QUEST2

def answer2(bot, update):
    answer = update.message.text
    if answer == "schatten" or "Schatten":
        update.message.reply_text("Richtig, danke für die Hilfe ma boy!")
        return
    else:
        update.message.text("Oh nein, du hast mich getöt!")
        return
    
def quest3(bot, update):
    update.message.text("Jo, ich hab noch eins!")
    update.message.text("Dort hängt es an der Wand, das gibt mir jeden moregen die Hand.")
    sleep(10000)
    update.message.text("Brauchst du einen Tipp?")
    answer = update.message.text
    if answer == "Ja" or "ja":
        update.message.text("Der Gegenstand befindet sich im Badezimmer.")
    return QUEST3

def answer3(bot, update):
     answer = update.message.text
    if answer == "Handtuch" or "handtuch":
        update.message.reply_text("Sehr gut, du bist ein schlaues Ding.")
        return
    else:
        update.message.text("Oh nein, du hast mich getöt!")
        return
    

def quest4(bot,update):
    update.message.text("Ich bin immernoch gefangen und ich stehe vor einem weiteren Rätsel wofür ich deine Hilfe benötige. Es ist echt schwer.")
    update.message.text("wer es macht, der sagt es nicht, \bwer es nimmt, der kennt es nicht, \bwer es kennt, der nimmt es nicht.")
    sleep(10000)
    update.message.text("Brauchst du einen Tipp?")
    answer = update.message.text
    if answer == "Ja" or "ja":
        update.message.text("Es hat etwas mit geld zu tun")
    return QUEST4
    
def answer4(bot, update):
     answer = update.message.text
    if answer == "Falschgeld" or "falschgeld" or "Blüten" or "blüten" or "Blüte" or "blüte" or "Spielgeld" or "spielgeld":
        update.message.reply_text("Bravo, das rätsel war etwas knifflig")
        return
    else:
        update.message.text("Oh nein, du hast mich getöt!")
        return
    

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

UNFINISHED, GETNAME, QUEST1, QUEST2, QUEST3, QUEST4 = range(6)

conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', intro)],
    states = {
        GETNAME: [MessageHandler(Filters.text, set_name)],
        UNFINISHED: [MessageHandler(Filters.text, quest1)],
        QUEST1: [MessageHandler(Filters.text, answer1)],
        QUEST2: [MessageHandler(Filters.text, answer2)],
        QUEST3: [MessageHandler(Filters.text, answer3)],
        QUEST4: [MessageHandler(Filters.text, answer4)]
    },
    fallbacks = [CommandHandler('reset', intro)]

)
