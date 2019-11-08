from bot.class_bot import Bot
from tokens import bot_token, weather_token
from time import sleep
import time
from parsers.currrate import BaseCurrRate as CurrRate
from parsers.habr import BaseHabr as Habr
from parsers.afisha import BaseAfisha as Afisha
from parsers.weather import BaseWeather as Weather


bot = Bot(bot_token)
currency = CurrRate()
habr = Habr()
afisha = Afisha()
weather = Weather()


while True:
    try:
        answer = bot.get_message()
        if answer is not None:
            chat_id = answer['chat_id']
            answer_text = answer['text']
            answer_text_words = answer_text.split()
            if 'ничего' in answer_text:
                bot.send_message(chat_id, 'Тогда проваливай')
            elif len(answer_text_words):
                if answer_text_words[0].upper() in ('/USD', '/EUR', '/RUB'):
                    if len(answer_text_words) == 1:
                        msg = currency.get_messages(answer_text_words[0][1:])
                        # if bot.last_status == 200:
                        if 1:
                            bot.send_message(chat_id, msg[0])
                        # else:
                        #     bot.send_message("Произошла ошибка {}".format(msg))
                    else:
                        day = int(answer_text_words[1])
                        month = int(answer_text_words[2])
                        year = int(answer_text_words[3])
                        dateiso = currency.date_to_iso(day, month, year)
                        msg = currency.get_messages(answer_text_words[0][1:],
                                              day, month, year)
                        # if bot.last_status == 200:
                        bot.send_message(chat_id, msg[0])
                        # else:
                        #     bot.send_message("Произошла ошибка {}".format(msg))
                elif answer_text_words[0].upper() == '/HABR':
                    if len(answer_text_words) == 1:
                        messages = habr.get_data()
                        bot.send_message(chat_id, '\n'.join(messages))
                    else:
                        bot.send_message(chat_id, habr.get_data(
                            int(answer_text_words[1])
                        ))
                elif answer_text_words[0].lower() == '/log':
                    num_messages = int(answer_text_words[1])
                    mes = bot.get_user_message(chat_id, num_messages)
                    if mes is not None:
                        bot.send_message(chat_id, f'{num_messages} сообщений назад ты писал(а): {mes}')
                elif answer_text_words[0].lower() == '/afisha':
                    messages = afisha.get_data()
                    # for mes in messages:
                    bot.send_message(chat_id, '\n'.join(messages))
                if answer_text_words[0] == '/courses':
                    if len(answer_text_words) == 1:
                        msg = currency.get_messages()
                        # if bot.last_status == 200:
                        if 1:
                            bot.send_message(chat_id, '\n'.join(msg))
                        # else:
                        #     bot.send_message("Произошла ошибка {}".format(msg))
                    else:
                        day = int(answer_text_words[1])
                        month = int(answer_text_words[2])
                        year = int(answer_text_words[3])
                        msg = currency.get_messages(None, day, month, year)
                        # if bot.last_status == 200:
                        bot.send_message(chat_id, '\n'.join(msg[0]))
                        # else:
                        #     bot.send_message("Произошла ошибка {}".format(msg))
                if answer_text_words[0] == '/weather':
                    msg = weather.get_message()
                    msg_city = weather.get_message_forecast()
                    bot.send_message(chat_id, msg)
                    bot.send_message(chat_id, msg_city)
        else:
            sleep(2)
    except Exception as e:
        # logging.error(type(e))
        print(type(e))
