import time

all = {}
highscores = []

def create(id, name):
    all[id] = {
        'name': name,
        'fails' : 0
    }

def migrateUser(oldID, newID):
    all[newID] = all[oldID]
    del all[oldID]

def add_fail(chat_id):
    if not all[chat_id]:
        create(chat_id,'unnamed')
    all[chat_id]['fails'] += 1

def start_time(chat_id):
    all[chat_id]['start_time'] = time.time()

def end_time(bot, chatId):
    user = all[chatId]
    diff_time = time.time() - user['start_time']
    bot.send_message(chat_id=chatId, text="Du hast " + str(diff_time/60) + " Minuten (+" + str(user['fails']) + " Fehler * 2 Minuten) gebraucht.")
    diff_time += user['fails'] * 120
    if len(highscores) == 0:
        highscores.append({'chat_id' : chatId, 'time' : diff_time, 'name' : user["name"]})
    index = False
    for score in highscores:
        if score['chat_id'] == chatId:
            if score['time'] < diff_time:
                score['time'] = diff_time
                return
        elif score['time'] < diff_time and not index:
            index = highscores.index(score)
    if index:
       highscores.insert(index,{'chat_id' : chatId, 'time' : diff_time, 'name' : user["name"]})
    if len(highscores) > 10:
        del highscores[-1]
