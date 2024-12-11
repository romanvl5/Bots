from datetime import timedelta
from telebot import types
from telebot.types import Message
import datetime as dt

#Кнопки
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttn1 = types.KeyboardButton('Забронировать время')
    buttn2 = types.KeyboardButton('Список бронирования')
    buttn3 = types.KeyboardButton('Отменить бронирование')
    buttn4 = types.KeyboardButton('Помощь')
    markup.add(buttn1, buttn2)
    markup.add(buttn3, buttn4)
    return markup

#Дата
def date_keyboard():
    now = dt.datetime.now()
    dates = []
    itembtns = []
    itembtns.clear()
    markup = types.ReplyKeyboardMarkup(row_width=4,one_time_keyboard=True)

    #запись на 12 дней
    for i in range(0,12):
        dates.append((now + timedelta(days=i)))

    #Список дат
    for date in dates:
        itembtn = types.KeyboardButton(str(date.date().day)+'/'+str(date.date().month))
        itembtns.append(itembtn)
    
    markup.add(itembtns[0],itembtns[1],itembtns[2],itembtns[3],itembtns[4],
    itembtns[5],itembtns[6],itembtns[7],itembtns[8],itembtns[9],itembtns[10],itembtns[11])
    return markup

#Время
def time_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True)
    itembtns = []
    #список
    time_slots = ['9:00','10:00','11:00','12:00','13:00','14:00',
                  '15:00','16:00','17:00','18:00','19:00','20:00','21:00']
    itembtns.clear()

    #список кнопок
    for time_slot in time_slots:
        itembtn = types.KeyboardButton(time_slot)
        itembtns.append(itembtn)

    #insert buttons into markup
    markup.add(itembtns[0],itembtns[1],itembtns[2],itembtns[3],itembtns[4],
    itembtns[5],itembtns[6],itembtns[7],itembtns[8],itembtns[9],
    itembtns[10],itembtns[11],itembtns[12])
    return markup

def remove_keyboard():
    markup = types.ReplyKeyboardRemove()
    return markup

