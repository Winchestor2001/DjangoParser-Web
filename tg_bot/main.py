# from aiogram import Bot, Dispatcher, types, executor
from telebot import types, TeleBot


BOT_TOKEN = '5843891649:AAGi5dUTveCKB2W3ij65w48tuEu3udAL1XI'
domain = '127.0.0.1:8000'
# bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
bot = TeleBot(token=BOT_TOKEN, parse_mode='html')
# dp = Dispatcher(bot)



@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    args = message.text
    args = args.split()
    user_id = message.from_user.id
    code, lang = args[1].split("___")
    username = message.from_user.username
    if code and code.lower() == username.lower():
        if lang != 'ru':
            bot.send_message(user_id, f"<a href='http://{domain}/{lang}/get_info/100'>Перейти</a>")
        else:
            bot.send_message(user_id, f"<a href='http://{domain}/get_info/100'>Перейти</a>")




if __name__ == '__main__':
    bot.infinity_polling()
    # executor.start_polling(dp, skip_updates=True)