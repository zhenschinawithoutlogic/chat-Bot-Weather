import requests  
import datetime  
import asyncio  # Модуль для работы с асинхронным программированием.
from config import open_weather_token, tg_bot_token 
from aiogram import Bot, Dispatcher  # Импортируем классы для работы с Telegram-ботом.
from aiogram.types import Message  # Класс для обработки входящих сообщений
from aiogram.filters import Command  # Фильтр для обработки команд 


# Инициализация бота 
bot = Bot(token=tg_bot_token)  # Создаем экземпляр бота, передавая токен для авторизации.
dp = Dispatcher()  # обработка сообщений


@dp.message(Command("start"))  #  связывает функцию с командой start
async def cmd_start(message: Message):  #  функция, которая выполняется при получении команды.
    user_first_name = message.from_user.first_name  # Получаем имя пользователя 
    await message.reply(f'Привет, {user_first_name}! Напиши город, а я скажу погоду!')  

# Хэндлер для получения погоды
@dp.message()  #связывает функцию с обработкой всех остальных сообщений.
async def get_weather(message: Message):  # функция для обработки запроса погоды.
    city = message.text  
    try:
        # Выполняем запрос к API OpenWeather
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru"
        )
        r.raise_for_status()  
        data = r.json()  # Преобразуем ответ от API в JSON-формат.

        # Извлекаем данные о погоде 
        city_name = data["name"] 
        cur_weather = data["main"]["temp"]  
        humidity = data["main"]["humidity"] 
        pressure = data["main"]["pressure"]  
        wind = data["wind"]["speed"]  
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')

       
        await message.reply(
            f"Погода в городе: {city_name}\n"
            f"🌡Температура🌡: {cur_weather}°C\n"
            f"🌧Влажность🌧: {humidity}%\n"
            f"☂️Давлениe☂️: {pressure} мм.рт.ст.\n"
            f"🌪Скорость ветра🌪: {wind} м/с\n"
            f"☀️Восход солнца☀️: {sunrise_timestamp}\n"
            f"Хорошего дня!"
        )
    except requests.exceptions.HTTPError as http_err:  # Обрабатываем ошибки запроса
        await message.reply(f"Ошибка, проверьте название города!") 
    except KeyError as key_err:  # Обрабатываем ошибки, если ключ отсутствует в ответе API
        await message.reply(f"Ошибка, проверьте название города!")  
    except Exception as ex:  # Ловим любые другие исключения
        await message.reply(f"Произошла ошибка: {ex}")  

# Основная функция для запуска бота
async def main():  
    print("Бот включен")  
    await dp.start_polling(bot)  

  
if __name__ == "__main__":  # Проверяем, что скрипт запущен как основная программа
    try:
        asyncio.run(main()) 
    except KeyboardInterrupt:  
        print('Бот выключен')  





















