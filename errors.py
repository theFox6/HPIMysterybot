from telegram.error import Unauthorized, TimedOut, ChatMigrated
import users

timeouts = 0

def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
        print("unauthorized")
    except TimedOut as e:
        if timeouts <= 10:
            print("Timeout!")
            timeouts += 1
        else:
            raise e
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
        print("chat " + update.chat_id + " migrated to " + e.new_chat_id)
        users.migrateUser(update.chat_id,e.new_chat_id)
