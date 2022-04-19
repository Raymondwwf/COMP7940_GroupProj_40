import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# The messageHandler is used for all message updates
import configparser
import logging
import pymysql
import base64
from PIL import Image
import io
import os
import requests

conn = pymysql.connect(host=os.environ['MYSQL_HOST'], port=int(
    os.environ['MYSQL_PORT']), user=os.environ['MYSQL_USER'], passwd=os.environ['MYSQL_PWD'], db=os.environ['MYSQL_DB'])
cursor = conn.cursor()
hikingid = None
comment = None
moviename = None
moviecomment = None
HIKESHARING, PHOTO = range(2)
COOKARYVIDEO = range(1)
MOVIENAME, MOVIEREVIEW = range(2)


def main():
    # Load your token and create an Updater for your Bot
    updater = Updater(
        token=(os.environ['TELE_TOKEN']), use_context=True)
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
                    'skipshare', skipsharephoto)
            ],
            PHOTO: [
                MessageHandler(Filters.photo, insertphoto), CommandHandler(
                    'viewhikeshare', viewhikeshare)
            ],
        },
        fallbacks=[CommandHandler('end', cancel)],
    )

    cookconv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            "cookshare", cookshare)],
        states={
            COOKARYVIDEO: [
                MessageHandler(Filters.video, cookaryshare)
            ],
        },
        fallbacks=[CommandHandler('end', cancel)],
    )

    movieconv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            "sharemovie", sharemovie)],
        states={
            MOVIENAME: [
                MessageHandler(Filters.text & (
                    ~Filters.command), sharemoviename)
            ],
            MOVIEREVIEW: [
                MessageHandler(Filters.text & (
                    ~Filters.command), sharemoviereview)
            ],

        },
        fallbacks=[CommandHandler('end', cancel)],
    )

    # register a dispatcher to handle message: here we register an echo dispatcher
    dispatcher.add_handler(CommandHandler("start", welcome))
    dispatcher.add_handler(CommandHandler("viewhikeshare", viewhikeshare))
    dispatcher.add_handler(CommandHandler("seemoviecomment", seereivew))
    dispatcher.add_handler(CommandHandler("skipshare", skipsharephoto))
    updater.dispatcher.add_handler(CallbackQueryHandler(userselected))
    dispatcher.add_handler(hikeconv_handler)
    dispatcher.add_handler(cookconv_handler)
    dispatcher.add_handler(movieconv_handler)

    # To start the bot:
    updater.start_polling()
    updater.idle()

# welcome menu


def welcome(update, context):
    welcome_message = '''hello, {}! Welcome to chatbot.
We have provided three features for you.
You can send /cookshare to share cooking video to us!
Or you can send /sharemovie to share cooking video to us!
Or you can select hiking to exploer hiking route from us! '''.format(
        update.message.from_user.first_name)
    reply_keyboard_markup = InlineKeyboardMarkup([
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
            "SELECT id,Trails,Path,RequireTime_Hours FROM hiking WHERE District=%s order by RAND() LIMIT 1", [callback_data])
        sqlresult = cursor.fetchall()
        for result in sqlresult:
            hikingid = result[0]
            trails = result[1]
            reqtime = result[3]
            path = result[2]
        selected_message = "Name:"+trails+"\nRoute:" + path+",\nTake Times:" + \
            str(reqtime)+"Hours\n You can use /hikeshare command to share the feeling of this route!"
        reply_keyboard_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text="Back to previous menu", callback_data="2")]
        ])

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=selected_message, reply_markup=reply_keyboard_markup)

# cookshare command


def cookshare(update, context):
    userid = update.message.from_user.id
    logging.info("User %s selected /cookshare", userid)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Nice! Please share the cooking video to us!!!! ")

    return COOKARYVIDEO

# hikeshare command


def hikeshare(update, context):
    userid = update.message.from_user.id
    logging.info("User %s selected /hikeshare", userid)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Great!Please input your sharing of this hiking route~~~")
    return HIKESHARING


# sharemovie command


def sharemovie(update, context):
    userid = update.message.from_user.id
    logging.info("User %s selected /sharemovie", userid)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Great!Please input the name of movie")
    return MOVIENAME

# sharemoviename


def sharemoviename(update, context):
    global moviename
    moviename = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s share movie name %s", userid, moviename)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Please input the review of movie")
    return MOVIEREVIEW

# sharemoviename


def sharemoviereview(update, context):
    global moviename, moviecomment
    moviecomment = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s share movie reivew %s", userid, moviecomment)
    cursor.execute(
        "INSERT INTO movieshare (moviename,moviesharing,userid) VALUES (%s,%s,%s)", (moviename, moviecomment, userid))
    conn.commit()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Thanks for your reivew sharing!!!")
    return ConversationHandler.END

# watch other user review


def seereivew(update, context):
    userid = update.message.from_user.id
    user = update.message.from_user
    try:
        cursor.execute(
            "SELECT moviename,moviesharing FROM movieshare WHERE userid<>%s order by RAND() LIMIT 1", (userid))
        sqlresult = cursor.fetchall()
        for result in sqlresult:
            moviename = result[0]
            moviesharing = result[1]
        conn.commit()
        conn.close()
        logging.info("User %s select to see review", user.first_name)
        reply_message = "Movie Name:"+moviename+"\nComment:" + moviesharing
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    return ConversationHandler.END


# share the cookary video


def cookaryshare(update, context):
    userid = update.message.from_user.id
    user = update.message.from_user
    logging.info("User %s shared cookary video to us", user.first_name)
    update.message.reply_text(
        'Thanks for sharing! Your cooking skill seems great!!!'
    )
    return ConversationHandler.END

# insert the hiking comment


def insertcomment(update, context):
    global hikingid
    global comment
    comment = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s inserted comment: %s ", userid, comment)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Great!More appericate to share image of it. or you can send /skipshare if you don\'t want to share!")
    return PHOTO

# insert the hiking photo and change it to blob to store in db


def insertphoto(update, context):
    global comment, hikingid
    """Stores the photo and asks for a location."""
    userid = update.message.from_user.id
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    path = photo_file.file_path
    #file = base64.b64encode(file)
    try:
        cursor.execute(
            "INSERT INTO hikecomment (hikingid,comment,photo,userid) VALUES (%s,%s,%s,%s)", (hikingid, comment, path, userid))
        conn.commit()
        logging.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
        update.message.reply_text(
            'Gorgeous! Now, you can send /viewhikeshare to watch other user sharing on this route.'
        )
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
        update.message.reply_text(
            'Please select the hiking distric first.'
        )
    return ConversationHandler.END

# cancel


def cancel(update, context) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logging.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! Have a nice day.'
    )
    return ConversationHandler.END


def skipsharephoto(update, context):
    print("TEST")
    global hikingid, comment
    comment = update.message.text
    userid = update.message.from_user.id
    try:
        cursor.execute(
            "INSERT INTO hikecomment (hikingid, comment,photo,userid) VALUES (%s,%s,NULL,%s)", (hikingid, comment, userid))
        conn.commit()
        conn.close()
        user = update.message.from_user
        logger.info("User %s did not send a photo.", user.first_name)
        update.message.reply_text(
            'Now, you can send /viewhikeshare to watch other user sharing on this route.'
        )
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    return ConversationHandler.END

# view other user hiking sharing


def viewhikeshare(update, context):
    global hikingid
    userid = update.message.from_user.id
    cursor.execute(
        "SELECT comment,photo FROM hikecomment WHERE hikingid=%s AND userid <>%s ORDER BY timestamp,RAND() DESC limit 1", (hikingid, userid))
    sqlresult = cursor.fetchall()
    comment = ""
    for result in sqlresult:
        comment = result[0]
        photo_path = result[1]
        reply_message = "The comment of hiking route from user:\n"+comment
        img_data = requests.get(photo_path).content
        with open('shatrephoto.jpg', 'wb') as handler:
            handler.write(img_data)
        print(reply_message)
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
        if photo_path is not None:
            context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=open('shatrephoto.jpg', 'rb'))
            if os.path.exists("shatrephoto.jpg"):
                os.remove("shatrephoto.jpg")


if __name__ == '__main__':
    main()
