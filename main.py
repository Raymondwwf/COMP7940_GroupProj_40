import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# The messageHandler is used for all message updates
import configparser
import logging
import hiking
import omdb
import pymysql


conn = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="project")
cursor = conn.cursor()
hikingid = None


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
    dispatcher.add_handler(CommandHandler("start", welcome))
    dispatcher.add_handler(CommandHandler("hikeshare", hikeshare))
    updater.dispatcher.add_handler(CallbackQueryHandler(userselected))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def welcome(update, context):
    welcome_message = '''hello, {}!Welcome to chatbot.
We have provided two features for you
lease Select. '''.format(
        update.message.from_user.first_name)
    reply_keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="TV show review", callback_data="1")],
        [InlineKeyboardButton(text="Hiking", callback_data="2")],
        [InlineKeyboardButton(
            text="Share your cooking video", callback_data="3")],

    ])
    user = update.message.from_user
    print('You talk with user {} and his user ID: {} '.format(
        user['username'], user['id']))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=welcome_message, reply_markup=reply_keyboard_markup)


def userselected(update, context):
    global hikingid
    callback_data = update.callback_query.data
    update.callback_query.answer()
    selected_message = ''
    reply_keyboard_markup = []
    if callback_data == "1":
        selected_message = 'Thanks for selecting TV show review! Do you want to Reading/writing a review?'
        reply_keyboard_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text="Reading a reviews.", callback_data="5")],
            [InlineKeyboardButton(
                text="writing a reviews to share.", callback_data="6")]
        ])
    if callback_data == "2":
        selected_message = 'Select the district. The system will recommend a route to you randomly.'
        reply_keyboard_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text="Kowloon", callback_data="kw")],
            [InlineKeyboardButton(
                text="HK Island", callback_data="hk")],
            [InlineKeyboardButton(
                text="NT", callback_data="nt")]
        ])
        print(hikingid)
    if callback_data == "5":
        selected_message = ''
    if callback_data == "6":
        print("writing")
    if callback_data == "kw" or callback_data == "hk" or callback_data == "nt":
        cursor.execute(
            "SELECT id,Trails,Path,RequireTime_Hours FROM hiking WHERE District=%s", [callback_data])
        sqlresult = cursor.fetchall()
        for result in sqlresult:
            hikingid = result[0]
            trails = result[1]
            reqtime = result[3]
            path = result[2]
        selected_message = "名稱:"+trails+"\n路線:" + \
            path+",\n需時:" + \
            str(reqtime)+"小時\n You can use /hikeshare command to share the feeling of this route!"
        reply_keyboard_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text="Back to previous menu", callback_data="2")]
        ])

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=selected_message, reply_markup=reply_keyboard_markup)


def hikeshare(update, context):
    global hikingid
    userid = update.message.from_user.id
    cursor.execute(
        "INSERT INTO hikecomment (hikingid, comment,userid) VALUES (%s,%s,%s)", (hikingid, update.message.text, userid))
    conn.commit()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Thanks for your sharing!")


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)


if __name__ == '__main__':
    main()
