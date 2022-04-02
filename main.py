import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# The messageHandler is used for all message updates
import configparser
import logging


def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(
        token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    # dispatcher.add_handler(CommandHandler("start", start))

    # To start the bot:
    updater.start_polling()
    updater.idle()


# def start(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text('hello, {}'.format(
#         update.message.from_user.first_name))


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)


if __name__ == '__main__':
    main()
