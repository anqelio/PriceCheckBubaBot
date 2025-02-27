# @PriceCheckBuba_bot
import telebot
import requests, bs4
from bs4 import BeautifulSoup
from telebot import types
import webbrowser

bot = telebot.TeleBot('8035323887:AAGGTRihmake6X0ehtAd3KJkMqXtAvz5Jgc') # токен @BotFather

@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup() # кнопки подсказки
    btn1 = types.InlineKeyboardButton('Помощь', callback_data = 'callback_help')
    btn2 = types.InlineKeyboardButton('Информация', callback_data = 'callback_info')
    markup.row(btn2)
    markup.row(btn1)
    bot.send_photo(message.chat.id, photo=open('photo.png', 'rb'))
    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.first_name}.</b> Это <u>бот</u> сервиса - <em>PriceCheck!</em>', parse_mode='html', reply_markup=markup)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # кнопки у текста
    btn1 = types.KeyboardButton('Помощь')
    btn2 = types.KeyboardButton('Найти товар')
    markup.row(btn2)
    markup.row(btn1)
    bot.send_message(message.chat.id, '<b>Выберите один из вариантов:</b>', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Помощь':
        helps(message)
    if message.text == 'Открыть страницу ВК':
        website(message)
    if message.text == 'Найти товар':
        product_category(message)

@bot.callback_query_handler(func=lambda call: call.data == 'callback_help')
def helps(call): # функция вызывающая рабочую инлайн-кнопку
    bot.send_message(call.message.chat.id, 'хелпа')

@bot.message_handler(commands=['help'])
def helps(message): # функция вызывающая рабочую кнопку
    bot.send_message(message.chat.id, 'хелпа')

@bot.callback_query_handler(func=lambda call: call.data == 'callback_info')
def info(call):
    bot.send_message(call.message.chat.id, 'Наша система проводит автоматизированный мониторинг цен, чтобы вы всегда были в курсе изменений. \n Вам больше не нужно вручную проверять различные сайты — просто введите название товара, и PriceCheck предоставит вам всю необходимую информацию.')

@bot.message_handler(commands=['website'])
def website(message): # открытие сайта
    webbrowser.open('https://vk.com/ankoppchik')

@bot.message_handler(commands=['category'])
def product_category(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_technic = types.KeyboardButton('Техника')
    btn_clothes = types.KeyboardButton('Одежда')
    btn_comparison = types.KeyboardButton('Сравнить цену')
    back = types.KeyboardButton('Вернуться в Главное меню')
    markup.row(btn_clothes, btn_technic)
    markup.row(btn_comparison)
    markup.row(back)
    bot.send_message(message.chat.id, f'<b>Выберите категорию товаров: </b>', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, click_catalog)

def click_catalog(message):
    if message.text == 'Техника':
        web_technic(message)
    elif message.text == 'Одежда':
        web_clothes(message)
    elif message.text == 'Сравнить цену':
        comparison(message)
    elif message.text == 'Вернуться в Главное меню':
        main(message)
    elif message.text in ['ДНС', 'М-видео', 'Ситилинк']:
        selected_store(message)
    elif message.text in ['КроссПарк', 'CodeRed', 'Gloria Jeans']:
        selected_store(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите опцию из меню.')

@bot.message_handler(commands=['web_technic'])
def web_technic(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    dns_btn = types.KeyboardButton('ДНС')
    m_video_btn = types.KeyboardButton('М-видео')
    citilink_btn = types.KeyboardButton('Ситилинк')
    back = types.KeyboardButton('Вернуться в Главное меню')
    markup.row(dns_btn, m_video_btn, citilink_btn)
    markup.row(back)
    bot.send_message(message.chat.id, f'<b>Выберите интернет-магазин: </b>', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, click_catalog)

@bot.message_handler(commands=['web_clothes'])
def web_clothes(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kp_btn = types.KeyboardButton('КроссПарк')
    cr_btn = types.KeyboardButton('CodeRed')
    gj_btn = types.KeyboardButton('Gloria Jeans')
    back = types.KeyboardButton('Вернуться в Главное меню')
    markup.row(kp_btn, gj_btn, cr_btn)
    markup.row(back)
    bot.send_message(message.chat.id, f'<b>Выберите интернет-магазин: </b>', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, click_catalog)

def selected_store(message):
    store = message.text
    bot.send_message(message.chat.id, f'Вы выбрали магазин: <b>{store}</b>', parse_mode='html')
    print('Выбор успешен')

    store_url = {
        'КроссПарк': 'https://krosspark.ru/',
        'CodeRed': 'https://codered.su/?ysclid=m7nhpw0v9g780658066',
        'Gloria Jeans': 'https://www.gloria-jeans.ru/',
        'DNS': 'https://www.dns-shop.ru/',
        'М-видео': 'https://www.mvideo.ru/',
        'Ситилинк': 'https://www.citilink.ru/'
    }

    selected_url = store_url.get(store)

    if selected_url:
        response = requests.get(selected_url)
        if response.status_code == 200:
            bot.send_message(message.chat.id, f'Запрос к <b>{store}</b> выполнен успешно! Данные получены.', parse_mode='html')
            print(f'Магазин найден - {store}')
        else:
            bot.send_message(message.chat.id, f'Не удалось получить данные из <b>{store}</b>. Статус: {response.status_code}', parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Выбранный магазин не найден.')
        print('Магазин не найден')

@bot.message_handler(commands=['comparison'])
def comparison(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_technic = types.KeyboardButton('Техника')
    btn_clothes = types.KeyboardButton('Одежда')
    back = types.KeyboardButton('Вернуться в Главное меню')
    markup.row(btn_clothes)
    markup.row(btn_technic)
    markup.row(back)
    bot.send_message(message.chat.id, f'<b>Выберите 1-ую категорию товаров: </b>', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, click_catalog)

bot.polling(none_stop=True)