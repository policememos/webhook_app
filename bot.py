import random
import os

import logging
from aiogram import Bot, Dispatcher, executor, types, asyncio
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove




bot = Bot(token=os.getenv('telebot'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


async def start(_):
    print("________________________________________________\n________________Bot is ONLINE___________________\n")
# Обрабатываем ошибку блока юзером
@dp.message_handler(commands="block")
async def cmd_block(message: types.Message):
    await asyncio.sleep(10.0)  # Здоровый сон на 10 секунд
    await message.reply("Вы заблокированы")
@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True

# Реакция на любое сообщение от юзера
# @dp.message_handler()
# async def namefun(message: types.Message):
#     await message.answer(f"Привет, {message.text}!")
    
    
# Реакция команду answer - сообщением
@dp.message_handler(commands='answer' ,commands_prefix = '3')
async def cmd_answer(message: types.Message):
    await message.answer("Это простой ответ")

# Реакция команду answer - ответом 
@dp.message_handler(commands="reply")
async def cmd_reply(message: types.Message):
    await message.reply('Это ответ с "ответом"')

# Реакция команду answer - кинуть emoji    
@dp.message_handler(commands="dice")
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="👋🏼")
    

# async def show_buttons(message: types.message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ["Да", "Нет"]
#     keyboard.add(*buttons)
#     await message.answer_dice(emoji="🎰")
#     await message.answer('Приветствую тебя в игрe black jack!',reply_markup=keyboard)
#     await message.answer('Сыграем?')

# @dp.message_handler(commands='start')
async def send_welcome(message: types.message): 
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Давай"]
    keyboard.add(*buttons)
    await message.answer_dice(emoji="🎰")
    await asyncio.sleep(1.0)
    await message.answer('Приветствую тебя в игрe black jack!')
    await asyncio.sleep(1.0)
    await message.answer('Сыграем?',reply_markup=keyboard)
    
    
    





#___________________________________________________________________________________________
    
     
# Функция на кнопку кнопку с текстом "давай"
async def with_puree(message: types.Message):
    # await message.answer('иии...', reply_markup=ReplyKeyboardRemove())
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.answer('Поеехали',reply_markup=keyboard)

    all_card = [6,7,8,9,10,'Валет','Дама','Король','Туз']
    all_mast = ['Пики','Червы', 'Бубны', 'Трефы']
    card_counter = 2
    card_counter_bot = 2
    card_sum = 0
    card_sum_bot = 0
    card_pool = [[x,y] for x in all_card for y in all_mast] 
    card_int1, card_int2 = 0,0  
  
    async def check(current_card):
        card = 0
        try:
            if current_card:
                card = current_card
                return card
    
        except:
            temp = {
                'Валет': 2,
                'Дама': 3,
                'Король': 4,
                'Туз': 11
                
            }
            if current_card in temp:
                card = temp[current_card]
                return card
            else:
                print('CHEK CARD ERROR')

    def randCard():
        nonlocal card_pool
        current_card = random.choice(card_pool)
        temp_pool = []
        for key in card_pool:
            index = card_pool.index(key)
            if key != current_card:
                temp_pool.append(key)
        card_pool = temp_pool   
        return current_card


    card_int1, card_int2 = randCard(), randCard()
    card_sum_bot = check(card_int1[0]) + check(card_int2[0])
    card_bot_pool = [card_int1,card_int2]

    card_int1, card_int2 = randCard(), randCard()
    card_sum = check(card_int1[0]) + check(card_int2[0])
    card_user_pool = [card_int1, card_int2]
    
    


    



#**********************STATA OF CARDS*********************
    def cardstat():
        #print(f'Сумма ваших карт: {card_sum}')
        message.answer(f'Сумма ваших карт: {card_sum}')
        message.answer(f'Сумма карт бота: {card_sum_bot}\n')
        message.answer('Ваши карты:')
        q=1
        for i in card_user_pool:
            message.answer(f"{q}) {i[0]}, масть '{i[1]}' ")
            q += 1
        message.answer('Карты бота:\n')
        q=1
        for i in card_bot_pool:
            message.answer(f"{q}) {i[0]}, масть '{i[1]}' ")
            q += 1


#*********************BOT AI*******************

    def botAI():
        nonlocal card_sum_bot
        nonlocal card_bot_pool
        nonlocal card_counter_bot
        while card_counter_bot < 6:
            current_card_bot = randCard()
            card_int_bot = check(current_card_bot[0])
            try_int = card_int_bot + card_sum_bot
            if try_int < 21:
                card_bot_pool.append(current_card_bot)
                card_sum_bot = try_int
                card_counter_bot += 1
            else:
                return card_sum_bot
        return card_sum_bot
    cardstat()


if __name__ == "__main__":
    dp.register_message_handler(send_welcome, commands='start')
    dp.register_message_handler(with_puree, Text(equals="Давай"))
    # Запуск бота
    executor.start_polling(dp, skip_updates=True, on_startup=start)