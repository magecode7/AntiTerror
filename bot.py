import logging
from aiogram import Bot, Dispatcher, executor, types
import reportgen
import messagedumper
import aiofiles
import os

TOKEN = ""
bot = Bot(token=TOKEN)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование
logging.basicConfig(filename='bot.log', level=logging.INFO)

    
PATH = "reports"
if not os.path.exists(PATH):
    os.makedirs(PATH)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь")
    ])

# Хэндлер на команду /start
@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    await set_default_commands(dp)
    await message.answer("Добро пожаловать! Я бот для обнаружения террористической информации в каналах. Просто отправте мне сообщение или ссылку на канал (https) для проверки")

#Стандартная обработка
@dp.message_handler()
async def message_handler(message: types.Message):
    text = message.text
    print(message.from_user.first_name, ':', text)

    path = f'{PATH}\\result_{str(message.from_user.id)}.txt'
    try:
        if text.startswith(('https', '@')): #Обработка ссылок
            await message.answer('Производится дамп сообщений, пожалуйста подождите...')
            channel = text
            texts = await messagedumper.dump_all_messages(channel)

            await message.answer(f'Произведен дамп {len(texts)} сообщений\nФормируем отчет...')

            await reportgen.create_report(texts, path)
            await message.answer('Отправка отчета...')

            async with aiofiles.open(path, 'rb') as file:
                await message.answer_document(file)

            await message.answer('Анализ окончен!')

            os.remove(path)
        else:
            # if len(text) < 30:
            #     await message.answer('Сообщение слишком короткое')
            #     return

            await reportgen.create_report([text], path)
            await message.answer('Отправка отчета...')

            async with aiofiles.open(path, 'rb') as file:
                await message.answer_document(file)

            await message.answer('Анализ окончен!')

            os.remove(path)
            
    except TypeError as e:
        print(e)
        await message.answer('Ошибка чтения :(')

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)



