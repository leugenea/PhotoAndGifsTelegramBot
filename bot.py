import logging

from telegram.ext.commandhandler import CommandHandler
from telegram.ext.regexhandler import RegexHandler
from telegram.ext.updater import Updater
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

import settings
from cv_wrap import get_picture
from moviepy_wrap import get_gif

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [["Gimme Scroll's photo", "Gimme Scroll's GIF"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

WANT_IMAGE = range(1)


def start(bot, update):
    update.message.reply_text('Hi!', reply_markup=markup)


def gimme_picture(bot, update):
    path_to_photo = get_picture()
    update.message.reply_photo(open(path_to_photo, 'rb'), reply_markup=markup)


def gimme_gif(bot, update):
    path_to_gif = get_gif()
    update.message.reply_document(open(path_to_gif, 'rb'), reply_markup=markup)


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(settings.TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(RegexHandler("^(Gimme(.*)(image|picture|photo))$", gimme_picture))
    dispatcher.add_handler(RegexHandler("^(Gimme(.*)(gif|GIF|Gif))$", gimme_gif))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
