import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# The messageHandler is used for all message updates
import configparser
import logging
import omdb
import pymysql
import base64
from PIL import Image
import io


conn = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="project")
cursor = conn.cursor()
hikingid = None
comment = None
HIKESHARING, PHOTO = range(2)
COOKARYVIDEO = range(1)


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
    hikeconv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            "hikeshare", hikeshare)],
        states={
            HIKESHARING: [
                MessageHandler(Filters.text & (~Filters.command), insertcomment), CommandHandler(
                    'skipsharing', skip_photo),
            ],
            PHOTO: [
                MessageHandler(Filters.photo, insertphoto), CommandHandler(
                    'viewhikeshare', viewhikeshare)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    cookconv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            "cookshare", cookshare)],
        states={
            COOKARYVIDEO: [
                MessageHandler(Filters.video, cookaryshare)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # register a dispatcher to handle message: here we register an echo dispatcher
    dispatcher.add_handler(CommandHandler("start", welcome))
    dispatcher.add_handler(CommandHandler("viewhikeshare", viewhikeshare))
    updater.dispatcher.add_handler(CallbackQueryHandler(userselected))
    dispatcher.add_handler(hikeconv_handler)
    dispatcher.add_handler(cookconv_handler)

    # To start the bot:
    updater.start_polling()
    updater.idle()

# welcome menu


def welcome(update, context):
    welcome_message = '''hello, {}!Welcome to chatbot.
We have provided two features for you
lease Select. Or you can send /cookshare to share cooking video to us! '''.format(
        update.message.from_user.first_name)
    reply_keyboard_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="TV show review", callback_data="1")],
        [InlineKeyboardButton(text="Hiking", callback_data="2")]
    ])
    user = update.message.from_user
    print('You talk with user {} and his user ID: {} '.format(
        user['username'], user['id']))
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=welcome_message, reply_markup=reply_keyboard_markup)

# indentify the user selection


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
                text="Reading a reviews.", callback_data="readmovieshare")],
            [InlineKeyboardButton(
                text="writing a reviews to share.", callback_data="movieshare")]
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
    if callback_data == "readmovieshare":
        selected_message = ''
    if callback_data == "movieshare":
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

# cookshare command


def cookshare(update, context):
    userid = update.message.from_user.id
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Great!Please input your sharing of this hiking route~~")
    return COOKARYVIDEO

# hikeshare command


def hikeshare(update, context):
    userid = update.message.from_user.id
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Great!Please input your sharing of this hiking route~~~")
    return HIKESHARING

# share the cookary video


def cookaryshare(update, context):
    userid = update.message.from_user.id
    user = update.message.from_user
    logging.info("User %s shared cookary video to us", user.first_name)
    update.message.reply_text(
        'Thanks for sharing!'
    )
    return ConversationHandler.END

# insert the hiking comment


def insertcomment(update, context):
    global hikingid
    global comment
    comment = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s inserted comment:%s", (userid, comment))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Great!More appericate to share image of it. or you can send /skipshare if you don\'t want to share!")
    return PHOTO

# insert the hiking photo and change it to blob to store in db


def insertphoto(update, context):
    global comment
    """Stores the photo and asks for a location."""
    userid = update.message.from_user.id
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    file = open(photo_file.download('user_photo.jpg'), 'rb').read()
    file = base64.b64encode(file)
    cursor.execute(
        "INSERT INTO hikecomment (hikingid,comment,photo,userid) VALUES (%s,%s,%s,%s)", (hikingid, comment, file, userid))
    conn.commit()
    logging.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Gorgeous! Now, you can send /viewhikeshare to watch other user sharing on this route.'
    )
    return ConversationHandler.END

# cancel


def cancel(update, context) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logging.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! Have a nice day.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def skip_photo(update, context):
    """Skips the photo and asks for a location."""
    global hikingid
    global comment
    comment = update.message.text
    userid = update.message.from_user.id
    cursor.execute(
        "INSERT INTO hikecomment (hikingid, comment,userid) VALUES (%s,%s,%s)", (hikingid, comment, userid))
    conn.commit()
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'Now, you can send /viewhikeshare to watch other user sharing on this route.'
    )
    return ConversationHandler.END

# view other user hiking sharing


def viewhikeshare(update, context):
    global hikingid
    userid = update.message.from_user.id
    cursor.execute(
        "SELECT comment,photo FROM hikecomment WHERE hikingid=%s AND userid <>%s ORDER BY timestamp DESC limit 1", (hikingid, userid))
    sqlresult = cursor.fetchall()
    comment = ""
    for result in sqlresult:
        comment = result[0]
    reply_message = "The comment of above hiking route from user:\n"+comment
    print(reply_message)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)


if __name__ == '__main__':
    main()
