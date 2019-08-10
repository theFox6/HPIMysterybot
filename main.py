from telegram.ext import Updater,CommandHandler, Filters
import story, errors, os, logging, hints
#import sys
from threading import Thread

with open("token.txt") as token_file:
    token = token_file.read().strip()

with open("owners.txt") as owner_file:
    owners = owner_file.readlines()

def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one"""
        updater.stop()
        logging.debug("stopped updater")
        #py_exec = '"' + sys.executable + '"'
        #os.execl(py_exec, py_exec, *sys.argv)
        os.system("python main.py")

    def restart(bot, update):
        print('Bot is restarting...')
        update.message.reply_text('Bot is restarting...')
        print(update.message.from_user.name + " requested a restart")
        Thread(target=stop_and_restart).start()

    dispatcher.add_handler(CommandHandler('restart', restart, filters=Filters.user(username=owners)))
    dispatcher.add_handler(story.conv_handler)
    dispatcher.add_handler(hints.callback_handler)
    dispatcher.add_error_handler(errors.error_callback)

    updater.start_polling()
    print("bot ready")
    updater.idle()

if __name__ == '__main__':
    main()
