import telebot
import requests
from requests import Response

import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
url = 'http://195.46.191.174:7777/ut/hs/tg_bot/'
login = 'tg_bot'
password = '123'


@bot.message_handler(commands=['start'])
def welcome(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
    keyboard.add(button_phone)  # Добавляем эту кнопку
    bot.send_message(message.chat.id, 'Здравствуйте, для начала работы укажите свой номер телефона', reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def registration(message):
    if message.contact is not None:

        params = 'phone_number=' + message.contact.phone_number + '&id=' + str(message.chat.id)
        req = requests.get(url + 'registration?'+ params, auth =(login, password))

        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, req.text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'Accept':

                params = 'message_id=' + str(call.message.id) + '&chat_id=' + str(call.message.chat.id) + '&chat_id=' + str(call.message.chat.id) + '&name=Accept'
                answer = requests.get(url + 'InlineKeyboardMarkup?' + params, auth=(login, password))

                if answer.text == "Успешно":
                    markup = types.InlineKeyboardMarkup(row_width=4)
                    item1 = types.InlineKeyboardButton("Прикрепить акт и завершить", callback_data='Complete')
                    item2 = types.InlineKeyboardButton("Счетчик снят", callback_data='CounterRemoved')
                    item3 = types.InlineKeyboardButton("Отказ", callback_data='RejectedCustomer')
                    item4 = types.InlineKeyboardButton("Отложить", callback_data='Postpone')

                    markup.add(item1, item2, item3, item4)

                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text=call.message.text,
                                          reply_markup=markup)
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                              text= answer.text )


            elif call.data == 'Complete':

                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Подключаем клавиатуру
                button_Complete = types.KeyboardButton(text="Завершить заявку")
                keyboard.add(button_Complete)  # Добавляем эту кнопку

                result = bot.send_message(call.message.chat.id,
                                 'Прикрепите фото документов, для завершения выполнения заявки:',
                                 reply_to_message_id=call.message.message_id, reply_markup=keyboard)

                params = 'message_id=' + str(result.message_id) + "&chat_id=" + str(call.message.chat.id) + '&parental_message_id=' + str(call.message.id) + '&name=Complete'
                requests.get(url + 'InlineKeyboardMarkup?' + params, auth=(login, password))

                markup = types.InlineKeyboardMarkup()
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                      text=call.message.text,
                                      reply_markup=markup)

                # # show alert
                # bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                #                           text="Завершение заявки")



            elif call.data == 'CounterRemoved':

                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Прикрепить акт и завершить", callback_data='Complete')

                markup.add(item1)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=call.message.text,
                                        reply_markup=markup)

                params = 'message_id=' + str(call.message.id) + '&chat_id=' + str(call.message.chat.id) + '&name=CounterRemoved'
                requests.get(url + 'InlineKeyboardMarkup?' + params, auth=(login, password))

            elif call.data == 'Reject':

                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Откланена заказчиком", callback_data='RejectedCustomer')
                item2 = types.InlineKeyboardButton("Заявка уже выполнена", callback_data='AlreadyCompleted')
                item3 = types.InlineKeyboardButton("Вернуться к заявке", callback_data='Cancellation')

                markup.add(item1, item2, item3)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=call.message.text,
                                      reply_markup=markup)

            elif call.data == 'RejectedCustomer':

                params = 'message_id=' + str(call.message.id) + '&chat_id=' + str(call.message.chat.id) + '&name=RejectedCustomer'
                requests.get(url + 'InlineKeyboardMarkup?' + params, auth=(login, password))

                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


            elif call.data == 'AlreadyCompleted':
                params = 'message_id=' + str(call.message.id) + '&chat_id=' + str(call.message.chat.id) + '&name=AlreadyCompleted'
                requests.get(url + 'InlineKeyboardMarkup?' + params, auth=(login, password))

                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            elif call.data == 'Cancellation':
                markup = types.InlineKeyboardMarkup(row_width=3)
                item1 = types.InlineKeyboardButton("Принять", callback_data='Accept')
                item2 = types.InlineKeyboardButton("Отклонить", callback_data='Reject')
                item3 = types.InlineKeyboardButton("Отложить", callback_data='Postpone')

                markup.add(item1, item2, item3)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=call.message.text,
                                      reply_markup=markup)

            elif call.data == 'Postpone':

                markup = types.InlineKeyboardMarkup(row_width=3)
                item1 = types.InlineKeyboardButton("Возобновить заявку", callback_data='EndWaiting')
                item2 = types.InlineKeyboardButton("Оплата по счету", callback_data='PaymentOnAccount')

                markup.add(item1, item2)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=call.message.text,
                                      reply_markup=markup)

                params = 'message_id=' + str(call.message.id) + '&chat_id=' + str(call.message.chat.id) + '&name=Postpone'
                requests.get(url + 'InlineKeyboardMarkup?' + params, auth=(login, password))

            elif call.data == 'EndWaiting':

                markup = types.InlineKeyboardMarkup(row_width=3)
                item1 = types.InlineKeyboardButton("Принять", callback_data='Accept')
                item2 = types.InlineKeyboardButton("Отклонить", callback_data='Reject')
                item3 = types.InlineKeyboardButton("Отложить", callback_data='Postpone')

                markup.add(item1, item2, item3)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=call.message.text,
                                      reply_markup=markup)

            elif call.data == 'PaymentOnAccount':
                params = 'message_id=' + str(call.message.id) + '&chat_id=' + str(call.message.chat.id) + '&name=PaymentOnAccount'
                requests.get(url + 'InlineKeyboardMarkup?' + params, auth=(login, password))

                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            # # remove inline buttons
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
            #                       reply_markup=None)



    except Exception as e:
        print(repr(e))

@bot.message_handler(content_types=['photo', 'document'])
def uploadphoto(message):

    if message.content_type == 'photo':

        result = len(message.photo)

        file_id = message.photo[result - 1].file_id
        params = 'message_id=' + str(message.id) + '&chat_id=' + str(message.chat.id) + '&file_id=' + str(file_id)
        requests.get(url + 'UploadPhoto?' + params, auth=(login, password))

        # bot.send_message(message.chat.id, req.text)
    elif message.content_type == 'document':

        file_id = message.document.file_id
        params = 'message_id=' + str(message.id) + '&chat_id=' + str(message.chat.id) + '&file_id=' + str(file_id)
        requests.get(url + 'UploadPhoto?' + params, auth=(login, password))

@bot.message_handler(content_types=['text'])
def CompletionApplication(message):

    if message.text == 'Завершить заявку':
        params = 'message_id=' + str(message.id) + '&chat_id=' + str(message.chat.id)
        requests.get(url + 'CompletionApplication?' + params, auth=(login, password))

        keyboard = types.ReplyKeyboardRemove()
        # bot.send_message(message.chat.id, 'Фото получены заявка закрыта',  reply_markup=keyboard)
        bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        # show alert
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                   text="Заявка завершена!")

#
#
# #RUN
bot.polling(none_stop=True)
