import telebot
import requests
import os
from telebot import types
import re
import openai
from style_guide import style_guide_men, style_guide_women 
import json
import csv

API_TOKEN = "8119951241:AAFK9e6IHq2B7iU8XDcTm-GU_KHd5LHNMrY"
bot = telebot.TeleBot(API_TOKEN)
API = 'e119fe20fcb94481b90174333230504'  # ключ для WeatherAPI

# Словарь для хранения состояния пользователя
user_states = {}

def greet_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    greet_button = types.KeyboardButton("👋 Поздороваться")
    markup.add(greet_button)
    return markup

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton("📋 Меню")
    profile_button = types.KeyboardButton("👤 Профиль")
    weather_button = types.KeyboardButton("🌦️ Погода")
    about_button = types.KeyboardButton("ℹ️ О боте")
    gid_button = types.KeyboardButton("🗺️ Гид по стилю")
    promotion_button = types.KeyboardButton("🎉 Акции и скидки")
    donate_button = types.KeyboardButton("💰 Скинуть денежку авторам на печеньки")
    support_button = types.KeyboardButton("🆘 Поддержка")
    markup.add(profile_button, weather_button, gid_button,promotion_button, donate_button,about_button, support_button)
    return markup

@bot.message_handler(commands=['start']) 
def main(message):
    bot.send_message(message.chat.id, f"👋 Привет, {message.from_user.first_name}! Добро пожаловать в нашего бота!\nЯ здесь, чтобы помочь вам с выбором одежды по погоде. 🌦️", reply_markup=greet_menu())

@bot.message_handler(func=lambda message: message.text == "👋 Поздороваться")
def greet_user(message):
    bot.send_message(message.chat.id, "Теперь выберите раздел:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "🌦️ Погода")
def ask_city(message):
    user_states[message.chat.id] = 'waiting_for_city'  # состояние ожидания
    bot.send_message(message.chat.id, "Напишите город, для которого хотите узнать погоду.")



# Меню
@bot.message_handler(func=lambda message: message.text == "👤 Профиль")
def user_info(message):
    user_id = message.from_user.id
    username = message.from_user.username or "Не указано"
    first_name = message.from_user.first_name or "Не указано"
    last_name = message.from_user.last_name or "Не указано"
    language_code = message.from_user.language_code or "Не указано"
    is_bot = message.from_user.is_bot

    info_text = (
        "👤 Информация о пользователе:\n"
        f"🔹 ID: {user_id}\n"
        f"🔹 Имя: {first_name}\n"
        f"🔹 Фамилия: {last_name}\n"
        f"🔹 Имя пользователя: @{username}\n"
        f"🔹 Язык: {language_code}\n"
    )
    bot.send_message(message.chat.id, info_text)


@bot.message_handler(func=lambda message: message.text == "ℹ️ О боте")
def about_bot(message):
    about_text = (
        "🤖 Приветствую вас в нашем уникальном боте, который поможет вам выбрать идеальную одежду в зависимости от погоды! 🌦️\n\n"
        "👗 Мы понимаем, как важно чувствовать себя комфортно и стильно в любое время года. Этот бот предоставляет вам рекомендации по одежде, основываясь на текущих погодных условиях в вашем городе.\n\n"
        "🌍 Независимо от того, идет ли дождь, светит солнце или дует холодный ветер, мы поможем вам подобрать подходящий наряд, чтобы вы всегда выглядели на все 100%! 💯\n\n"
        "🚀 Этот бот — это будущий стартап молодых разработчиков, которые стремятся сделать вашу жизнь проще и удобнее. Мы верим, что технологии могут помочь людям принимать более осознанные решения в повседневной жизни. 💡\n\n"
        "💬 Если у вас есть вопросы, предложения или идеи, как улучшить нашего бота, не стесняйтесь обращаться к нам! Мы всегда открыты для обратной связи и готовы развиваться вместе с вами.\n\n"
        "✨ Присоединяйтесь к нашему сообществу и будьте в курсе последних модных тенденций и погодных условий! Ваш стиль — наша забота! 🌟"
    )
    bot.send_message(message.chat.id, about_text)




@bot.message_handler(func=lambda message: message.text == "🗺️ Гид по стилю")
def gid(message):
    about_gid = (
        "🤖: Привет! Я искусственный интеллект и ваш гид по стилю! 🌟\n\n"
        "💡 Я генерирую идеи, чтобы сделать ваш стиль уникальным и запоминающимся!\n\n"
        "⚠️ Каждый день доступны новые идеи. Давайте создадим ваш идеальный стиль! 💃✨"
    )
    bot.send_message(message.chat.id, about_gid)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🕴️ Мужской"), types.KeyboardButton("👗 Женский"))
    bot.send_message(message.chat.id, "Выберите пол", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["🕴️ Мужской", "👗 Женский"])
def choose_style(message):
    user_states[message.chat.id] = "waiting_for_style_question"  # Установите новое состояние
    style_guide_selected = style_guide_men if message.text == "🕴️ Мужской" else style_guide_women
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for question in style_guide_selected.keys():
        markup.add(types.KeyboardButton(question))
    markup.add(types.KeyboardButton("🔙 Назад в меню"))
    bot.send_message(message.chat.id, "Выберите вопрос, который вас интересует:", reply_markup=markup)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_style_question")
def answer_style_quest(message):
    answer = None
    if message.text in style_guide_men:
        answer = style_guide_men[message.text]
    elif message.text in style_guide_women:
        answer = style_guide_women[message.text]
    
    if answer:
        bot.send_message(message.chat.id, answer)
    else:
        # Если вопрос не найден, просто возвращаем к выбору вопросов
        bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=main_menu())
        user_states[message.chat.id] = None  # Сброс состояния после возврата

@bot.message_handler(func=lambda message: message.text == "🔙 Назад в меню")
def back_to_main(message):
    bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=main_menu())
    user_states[message.chat.id] = None  # Сброс состояния после возврата в главное меню





@bot.message_handler(func=lambda message: message.text == "🎉 Акции и скидки")
def promotions(message):
    about_sale = (
        "Мы всегда стремимся предложить вам лучшие условия и возможности! В данный момент мы работаем над новой подпиской, которая позволит вам получать эксклюзивные рекомендации по одежде, специальные предложения и скидки на товары от наших партнеров! 🛍️✨\n\n"
        "Подписка будет доступна в ближайшее время, и мы уверены, что она сделает ваш опыт еще более увлекательным и выгодным! \n\n"
        "Следите за обновлениями, чтобы не пропустить запуск! 🚀"
    )
    bot.send_message(message.chat.id, about_sale)



def payment_menu(message):
    keyboard = types.InlineKeyboardMarkup()

    # Кнопки для платежных систем
    button_tinkoff = types.InlineKeyboardButton(text="💳 Тинькофф", callback_data="tinkoff")
    button_donation = types.InlineKeyboardButton(text="DonationAlerts 💖", url="https://www.donationalerts.com/r/ruslan_kulikov")
    
    keyboard.add(button_tinkoff, button_donation)
    bot.send_message(message.chat.id, "Выберите платежную систему:", reply_markup=keyboard)

# Функция для обновления клавиатуры с суммами
def update_amount_menu(call):
    keyboard = types.InlineKeyboardMarkup()

    button_100 = types.InlineKeyboardButton(text="100 RUB", url="https://www.tbank.ru/cf/9uwIZw2IzAI?amount=100")
    button_500 = types.InlineKeyboardButton(text="500 RUB", url="https://www.tbank.ru/cf/9uwIZw2IzAI?amount=500")
    button_1000 = types.InlineKeyboardButton(text="1000 RUB", url="https://www.tbank.ru/cf/9uwIZw2IzAI?amount=1000")
    button_other = types.InlineKeyboardButton(text="Любая другая сумма 💸", url="https://www.tbank.ru/cf/9uwIZw2IzAI")
    keyboard.add(button_100, button_500, button_1000, button_other)

    # Кнопка "Назад"
    back_button = types.InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_payment")
    keyboard.add(back_button)

    # Обновляем текущее сообщение
    bot.edit_message_text("Выберите сумму для пополнения:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

# Функция для обновления меню с платежными системами
def update_payment_menu(call):
    keyboard = types.InlineKeyboardMarkup()

    # Кнопки для платежных систем
    button_tinkoff = types.InlineKeyboardButton(text="💳 Тинькофф", callback_data="tinkoff")
    button_donation = types.InlineKeyboardButton(text="DonationAlerts 💖", url="https://www.donationalerts.com/r/ruslan_kulikov")
    
    keyboard.add(button_tinkoff, button_donation)

    # Обновляем текущее сообщение
    bot.edit_message_text("Выберите платежную систему:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "💰 Скинуть денежку авторам на печеньки")
def donat(message):
    payment_menu(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data in ["tinkoff", "sber", "ozon"]:
        update_amount_menu(call)
    elif call.data == "back_to_payment":
        update_payment_menu(call)

@bot.message_handler(func=lambda message: message.text == "🆘 Поддержка")
def support_textbot(message):
    support_text = (
        "Если у вас возникли вопросы, предложения или идеи для дальнейшего развития нашего бота, не стесняйтесь писать нам! Мы всегда открыты для обратной связи и готовы улучшать наш сервис.\n\n"
        "📩 Пишите @mlnkrr, и мы постараемся ответить вам как можно скорее!"
    )
    bot.send_message(message.chat.id,support_text)






# получение Апишки
@bot.message_handler(func=lambda message:user_states.get(message.chat.id)=="waiting_for_city")
def get_weather(message):

    # Проверяем находится ли пользователь в состоянии ожидания ввода города
        city = message.text.strip().lower()
        print(f"Получен запрос на погоду для города: {city}")  # Логирование
        try:
            res = requests.get(f'https://api.weatherapi.com/v1/current.json?key={API}&q={city}&aqi=no', timeout=60)
            print(f"Статус код ответа: {res.status_code}")  # Логирование статуса ответа
            
            if res.status_code == 200:
                data = res.json() 
                print(f"Данные о погоде: {data}")  # Логирование данных
                
                if "current" in data:
                    temperature = data["current"]["temp_c"]
                    humidity = data["current"]["humidity"]
                    wind_speed = data["current"]["wind_kph"]
                    feel_weather = data["current"]["feelslike_c"]
                    weather_description = data["current"]["condition"]["text"] 

                    if 'clear' in weather_description.lower():
                        image_path = 'photo/sun (1).jpg'
                    elif 'sunny' in weather_description.lower():
                        image_path = 'photo/sun (1).jpg'
                    elif 'overcast' in weather_description.lower():
                        image_path = 'photo/cloudy.jpg'
                    elif 'fog' in weather_description.lower():
                        image_path = 'photo/cloudy.jpg'    
                    elif 'mist' in weather_description.lower():
                        image_path = 'photo/cloudy.jpg'
                    elif 'cloud' in weather_description.lower(): 
                        image_path = 'photo/cloudy.jpg'
                    elif 'rain' in weather_description.lower():
                        image_path = 'photo/rain.jpg'
                    elif 'snow' in weather_description.lower():
                        image_path = 'photo/m028t0163_l_black_cloud_with_snow_and_moon_28sep22.jpg'
                    elif 'wind' in weather_description.lower():
                        image_path = 'photo/m028t0163_o_windy_black_cloud_28sep22'
                    else:
                        image_path = None
                    
                    # Отправка фото, если оно существует
                    if image_path and os.path.exists(image_path):
                        with open(image_path, 'rb') as file:
                            bot.send_photo(message.chat.id, file)
                    
                    # Логирование извлеченных данных
                    print(f"Температура: {temperature}, Влажность: {humidity}, Скорость ветра: {wind_speed}, Ощущается как: {feel_weather}, Описание: {weather_description}")
                    
                 
                    text_response = (f'Сейчас погода в {city.title()}👇:\n'
                                     f'🌡️ Температура: {temperature}°C\n'
                                     f'💨 Скорость ветра: {wind_speed} км/ч\n'
                                     f'💧 Влажность: {humidity}%\n'
                                     f'💁 Ощущается как: {feel_weather}°C\n'
                                     f'☁️ Описание: {weather_description}')
            
                    bot.send_message(message.chat.id, text_response)
                else:
                    bot.reply_to(message, "Не удалось получить данные о погоде. Проверьте название города.")
            else:
                bot.reply_to(message, "Не удалось получить данные о погоде. Проверьте название города.")
        except requests.exceptions.ReadTimeout:
            bot.reply_to(message, "Запрос к API превысил время ожидания. Попробуйте позже.")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {str(e)}")
            print(f"Ошибка: {str(e)}")  # Логирование
        
        # Сбрасываем состояние после обработки
        user_states[message.chat.id] = "waiting_for_city"

bot.polling(non_stop=True, interval=0)