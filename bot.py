import telebot
import firestore_service
import keyboard

from booking import Booking
from bottoken import TOKEN
from firestore_service import booking_list

import time
import emoji
import datetime as dt

bot = telebot.TeleBot(token=TOKEN)


#/start
@bot.message_handler(commands=['start'])
def send_welcome(message):

    try:
        bot.send_message(chat_id=message.chat.id,
        text='''Привет!\n
С помощью этого бота ты можешь забронировать удобное для тебя время.\n
Используй команду /help чтобы посмотреть все команды бота или используй предложенные кнопки  ''',
#keyboard
        reply_markup=keyboard.main_keyboard()
        )
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Что-то пошло не так... \nПопробуй снова!'
        )


#Бронирование /book
@bot.message_handler(commands=['book'])

def register(message):
    date = ''
    try:
        new_booking = Booking()
        
        def get_name(message):
            try:
                check_input(message.text)
                new_booking.name = message.text
                bot.send_message(chat_id=message.chat.id, text='Введи номер телефона')
                #if triggered, go to get_phonenumber method
                bot.register_next_step_handler(message,get_phonenumber)
            except:
                bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так... \nПопробуй снова!',reply_markup=keyboard.main_keyboard())

        def get_phonenumber(message):
            try:
                check_input(message.text)
                new_booking.phone_number = message.text
                bot.send_message(chat_id=message.chat.id, 
                text='Выбери дату',
                reply_markup=keyboard.date_keyboard()
                )
                #if triggered, go to get_date method
                bot.register_next_step_handler(message,get_date)
            except:
                bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так... \nПопробуй снова!',reply_markup=keyboard.main_keyboard())

        def get_date(message):
            try:
                check_input(message.text)
                nonlocal date
                date = message.text
                bot.send_message(chat_id=message.chat.id,text='Выбери время',reply_markup=keyboard.time_keyboard())
                #if triggered, go to get_time method
                bot.register_next_step_handler(message,get_time)
            except:
                bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так... \nПопробуй снова!',reply_markup=keyboard.main_keyboard())

        def get_time(message):
            try:
                check_input(message.text)
                hour = message.text
                converted_time = convert_string_to_datetime(date,hour)
                exist = False
                same_time = 0
                #check if user_id already exist. if exist, cannot register
                for booking in booking_list:
                    if booking.user_id==message.from_user.id:
                        exist = True
                        break
                    if booking.time_slot == converted_time.timestamp():
                        same_time +=1
                if not exist:
                    #check if timeslot is full (default value is 1). if full, cannot register
                    if(same_time < 1):
                        new_booking.time_slot = int(converted_time.timestamp())
                        new_booking.user_id = message.from_user.id
                        firestore_service.add_booking(new_booking)
                        bot.send_message(chat_id=message.chat.id, text='Бронирование успешно!',reply_markup=keyboard.main_keyboard())
                    else:
                        bot.send_message(chat_id=message.chat.id, text='На это время не осталось мест!',reply_markup=keyboard.main_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id, text='Ваш аккаунт уже забронировал время',reply_markup=keyboard.main_keyboard())
            except:
                bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так... \nПопробуй снова!',reply_markup=keyboard.main_keyboard())
        
        #Начало
        bot.send_message(chat_id=message.chat.id, text='Введи свое имя', reply_markup=keyboard.remove_keyboard())
        bot.register_next_step_handler(message,get_name)
    
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Что-то пошло не так... \nПопробуй снова!',
        reply_markup=keyboard.main_keyboard()
        )

#Список бронирования /bookinglist
@bot.message_handler(commands=['bookinglist'])
def send_booking_list(message):
    try:
        delete_past_booking()
        bot.send_message(chat_id=message.chat.id,text=firestore_service.display,
        reply_markup=keyboard.main_keyboard())
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Что-то пошло не так... \nПопробуй снова!',
        reply_markup=keyboard.main_keyboard()
        )

#Отменить бронирование /withdraw
@bot.message_handler(commands=['withdraw'])
def send_Message(message):
    try:
        
            #check if booking connected to the user_id exist. return true if exist
            can_delete = firestore_service.delete_booking_by_userid(message.from_user.id)
            if can_delete:
                bot.send_message(chat_id=message.chat.id, text='Бронирование отменено',
                reply_markup=keyboard.main_keyboard())
            else:
                bot.send_message(chat_id=message.chat.id, text='Бронирований для удаления еще нет!',
                reply_markup=keyboard.main_keyboard())
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Что-то пошло не так... \nПопробуй снова!',
        reply_markup=keyboard.main_keyboard()
        )

#Помощь /help
@bot.message_handler(commands=['help'])
def send_help(message):
    try:
        bot.send_message(chat_id=message.chat.id,text=
        '''
        Как пользоваться ботом\n
Забронировать время /book\n
Проверить список бронирования /bookinglist\n
Отменить бронирование /withdraw\n
        ''',
        reply_markup=keyboard.main_keyboard()
        )
    except:
        bot.send_message(chat_id=message.chat.id,
        text='Что-то пошло не так... \nПопробуй снова!',
        reply_markup=keyboard.main_keyboard()
            )  


#Ответы на кнопки
@bot.message_handler(content_types=['text'])
def send_answers(message):
    date = ''
    #Бронь
    if (message.text == "Забронировать время"):
        new_booking = Booking()
        #Имя
        def get_name(message):
            try:
                check_input(message.text)
                new_booking.name = message.text
                bot.send_message(chat_id=message.chat.id, text='Введи номер телефона')
                #if triggered, go to get_phonenumber method
                bot.register_next_step_handler(message,get_phonenumber)
            except:
                bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так... \nПопробуй снова!',reply_markup=keyboard.main_keyboard())
        #Телефон
        def get_phonenumber(message):
            try:
                check_input(message.text)
                new_booking.phone_number = message.text
                bot.send_message(chat_id=message.chat.id, 
                text='Выбери дату',
                reply_markup=keyboard.date_keyboard()
                )
                #if triggered, go to get_date method
                bot.register_next_step_handler(message,get_date)
            except:
                bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так... \nПопробуй снова!',reply_markup=keyboard.main_keyboard())
        #Дата
        def get_date(message):
            try:
                check_input(message.text)
                nonlocal date
                date = message.text
                bot.send_message(chat_id=message.chat.id,text='Выбери время',reply_markup=keyboard.time_keyboard())
                #if triggered, go to get_time method
                bot.register_next_step_handler(message,get_time)
            except:
                bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так... \nПопробуй снова!',reply_markup=keyboard.main_keyboard())
        #Время
        def get_time(message):
            try:
                check_input(message.text)
                hour = message.text
                converted_time = convert_string_to_datetime(date,hour)
                exist = False
                same_time = 0
                #check if user_id already exist. if exist, cannot register
                for booking in booking_list:
                    if booking.user_id==message.from_user.id:
                        exist = True
                        break
                    if booking.time_slot == converted_time.timestamp():
                        same_time +=1
                if not exist:
                    #check if timeslot is full (default value is 1). if full, cannot register
                    if(same_time < 1):
                        new_booking.time_slot = int(converted_time.timestamp())
                        new_booking.user_id = message.from_user.id
                        firestore_service.add_booking(new_booking)
                        bot.send_message(chat_id=message.chat.id, text='Бронирование успешно!',reply_markup=keyboard.main_keyboard())
                    else:
                        bot.send_message(chat_id=message.chat.id, text='На это время не осталось мест!',reply_markup=keyboard.main_keyboard())
                else:
                    bot.send_message(chat_id=message.chat.id, text='Ваш аккаунт уже забронировал время',reply_markup=keyboard.main_keyboard())
            except:
                bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так... \nПопробуй снова!',reply_markup=keyboard.main_keyboard())
        #Начало
        bot.send_message(chat_id=message.chat.id, text='Введи свое имя',reply_markup=keyboard.remove_keyboard())
        bot.register_next_step_handler(message,get_name) 

    #Список бронирования кнопка
    elif (message.text == "Список бронирования"):
        delete_past_booking()
        bot.send_message(chat_id=message.chat.id,text=firestore_service.display,
        reply_markup=keyboard.main_keyboard())

    #Отменить бронирование кнопка
    elif (message.text == "Отменить бронирование"):
            #check if booking connected to the user_id exist. return true if exist
            can_delete = firestore_service.delete_booking_by_userid(message.from_user.id)
            if can_delete:
                bot.send_message(chat_id=message.chat.id, text='Бронирование отменено',
                reply_markup=keyboard.main_keyboard())
            else:
                bot.send_message(chat_id=message.chat.id, text='Бронирований для удаления еще нет!',
                reply_markup=keyboard.main_keyboard())
    
    #Помощь кнопка
    elif (message.text == "Помощь"):
            bot.send_message(chat_id=message.chat.id,text=
            '''
            Как пользоваться ботом\n
Забронировать время /book\n
Проверить список бронирования /bookinglist\n
Отменить бронирование /withdraw\n
            ''',
            reply_markup=keyboard.main_keyboard()
            )

    #Ошибка
    else:
        bot.send_message(chat_id=message.chat.id,
        text='Что-то пошло не так... \nПопробуй снова!',
        reply_markup=keyboard.main_keyboard()
        )
        

#convert string of date and time to datetime format
def check_input(text):
    #check if emoji
    if(text=='' or text[0][:1]=='/' or bool(emoji.get_emoji_regexp().search(text))):
        print('raising')
        raise Exception

#delete booking that already past time now
def delete_past_booking():
    time_now = dt.datetime.now()
    for booking in booking_list:
        if booking.datetime < time_now:
            firestore_service.delete_booking_by_documentid(booking.id)

#check text input from gif/emoji/empty string to prevent any error
#throw exception if false
def convert_string_to_datetime(date,hour):
    time_now = dt.datetime.now()       
    year = ''
    prob_date = dt.datetime.strptime(date+'/'+str(time_now.year),r'%d/%m/%Y')
    if(prob_date<time_now):
        year = str(time_now.year+1)
    else:
        year = str(time_now.year)
    date += '/'+ str(year)
    time = date + ' ' + hour
    converted_time = dt.datetime.strptime(time,r'%d/%m/%Y %H:%M')
    return converted_time

while True:
    try:
        bot.polling(none_stop=False)
    except Exception:
        print('crash')
        time.sleep(6)