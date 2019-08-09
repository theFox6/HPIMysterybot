from telegram.ext import Updater,CommandHandler
import story, errors
import os
#import sys
from threading import Thread

with open("token.txt") as token_file:
    token = token_file.read().strip()

def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        print("stopped updater")
        #py_exec = '"' + sys.executable + '"'
        #os.execl(py_exec, py_exec, *sys.argv)
        os.system("python main.py")

    def restart(bot, update):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()

    # FIXME add filters=Filters.user(username='@jh0ker')
    dispatcher.add_handler(CommandHandler('restart', restart))
    dispatcher.add_handler(story.conv_handler)
    dispatcher.add_error_handler(errors.error_callback)

    updater.start_polling()
    print("bot ready")
    updater.idle()

if __name__ == '__main__':
    main()
