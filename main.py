from telegram.ext import Updater
import story

with open("token.txt") as token_file:
    token = token_file.read().strip()

def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(story.conv_handler)

    updater.start_polling()
    print("bot ready")
    updater.idle()

if __name__ == '__main__':
    main()
