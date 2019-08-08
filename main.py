from telegram.ext import Updater
import story, errors

with open("token.txt") as token_file:
    token = token_file.read().strip()

def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(story.conv_handler)
    dispatcher.add_error_handler(errors.error_callback)

    updater.start_polling()
    print("bot ready")
    updater.idle()

if __name__ == '__main__':
    main()
