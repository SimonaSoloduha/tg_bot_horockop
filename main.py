import os
from dotenv import load_dotenv

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from buttons import button_appendix, znaki_zodiaka_inline, button_compatibility, button_yes, to_day_inline
from messages import HOROSCOPE_COMPATIBILITY, HOROSCOPE_TOMORROW, HOROSCOPE_ABOUT, HOROSCOPE_FOR_ONE, HOROSCOPE_FOR_ALL, \
    HOROSCOPE_ABOUT_APPENDIX, MASSAGES_HOROSCOPE_ABOUT, HOROSCOPE_COMPATIBILITY_YES, HOROSCOPE_COMPATIBILITY_SHE, \
    HOROSCOPE_TODAY

from parser import parse_horoscope_for_all, parse_horoscope_for_zodiac, parse_horoscope_compatibility


load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN, parse_mode='HTML')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


def get_start_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=HOROSCOPE_TODAY), KeyboardButton(text=HOROSCOPE_TOMORROW)],
        [KeyboardButton(text=HOROSCOPE_COMPATIBILITY), KeyboardButton(text=HOROSCOPE_ABOUT)],
    ]
    start_keyboard = ReplyKeyboardMarkup(keyboard=kb,
                                         resize_keyboard=True,
                                         input_field_placeholder="Выберите гороскоп")
    return start_keyboard


# Выбор гороскопа
@dp.message_handler(commands="start")
async def bot_start(msg: Message):
    await msg.answer("Здравстуй, дорогой!\nГадалка баба Сима рада тебя видеть 💋 \n\nТы так похорошел 👀\n\n"
                     f"{msg.from_user['first_name']}, cейчас тебе все расскажу, покажу, предскажу\n\n")
    await msg.answer("С чего начнем?\n(Жми кнопку ниже)",
                     reply_markup=get_start_keyboard())


# На сегодня / на завтра
@dp.message_handler(text=[HOROSCOPE_TODAY, HOROSCOPE_TOMORROW])
async def get_horoscope_today_or_tomorrow(msg: Message, state: FSMContext):
    horoscope_type = msg.text
    await state.update_data(horoscope_type=horoscope_type)
    await bot.send_sticker(chat_id=msg.from_user.id,
                           sticker=r"CAACAgIAAxkBAAEHugdj6kB-vghC45TQdY7Orfzr7r0GMgACSwADHSyIEAlSEdc6e9GbLgQ")
    await msg.answer(
        f'И скажи, моя хорошая, {horoscope_type.lower()[1::]} смотрим для всех или для одного знака? 👀',
        reply_markup=to_day_inline)


# Для одного
@dp.callback_query_handler(text=HOROSCOPE_FOR_ONE)
async def get_horoscope_for_one(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(horoscope_for=HOROSCOPE_FOR_ONE)
    await callback.message.answer(f'Хорошо, дорогой, теперь выбери знак зодиака', reply_markup=znaki_zodiaka_inline)


# Для всех
@dp.callback_query_handler(text=HOROSCOPE_FOR_ALL)
async def get_horoscope_for_all(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(horoscope_for=HOROSCOPE_FOR_ALL)
    user_data = await state.get_data()
    horoscope_type = user_data.get('horoscope_type')
    if horoscope_type == HOROSCOPE_TODAY:
        day = 'today'
    else:
        day = 'tomorrow'
    horoscope = parse_horoscope_for_all(day)
    await callback.message.answer(f'{horoscope_type} для всех:\n\n')
    await callback.message.answer(horoscope)


# Характеристика
@dp.message_handler(text=HOROSCOPE_ABOUT)
async def get_horoscope_about(msg: types.Message, state: FSMContext):
    await state.update_data(horoscope_type=HOROSCOPE_ABOUT)
    await bot.send_sticker(chat_id=msg.from_user.id,
                           sticker=r"CAACAgIAAxkBAAEHuftj6j-9QNmF1vzjEWfaw2c4BJ5IAgACKwADHSyIEK0mOYz9LdfMLgQ")
    await msg.answer(f'Хочешь узнать всю правду про конкретный знак?', reply_markup=button_yes)


# Характеристика дополнение
@dp.callback_query_handler(text=HOROSCOPE_ABOUT_APPENDIX)
async def get_horoscope_about_appendix(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    zodiac = user_data.get('zodiac')
    appendix = MASSAGES_HOROSCOPE_ABOUT[zodiac]['appendix']
    await callback.message.answer(appendix)


# Совместимости
@dp.message_handler(text=HOROSCOPE_COMPATIBILITY)
async def get_horoscope_compatibility(msg: Message, state: FSMContext):
    await state.update_data(horoscope_type=HOROSCOPE_COMPATIBILITY)
    await bot.send_sticker(chat_id=msg.from_user.id,
                           sticker=r"CAACAgIAAxkBAAEHrm5j536V_vJWvdZ_4uR3pPEBHGZxBgACEQADHSyIEEmpmwABW2ZL_i4E")
    await msg.answer(f'Ой ой ой) А кто-то у нас влюбился?', reply_markup=button_compatibility)


# Совместимости он
@dp.callback_query_handler(text=HOROSCOPE_COMPATIBILITY_YES)
async def get_horoscope_compatibility_he(callback: types.CallbackQuery):
    await callback.message.answer(f'Теперь давай серьезно, зайка моя. Кто ОН по гороскопу?',
                                  reply_markup=znaki_zodiaka_inline)


# гороском для знака
@dp.callback_query_handler(text_startswith="znak_")
async def get_horoscope_for_zodiac(callback: types.CallbackQuery, state: FSMContext):
    zodiac = callback.data.split("_")[1]
    user_data = await state.get_data()

    horoscope_type = user_data.get('horoscope_type')
    horoscope_compatibility_he = user_data.get('horoscope_compatibility_he')
    try:
        await state.update_data(zodiac=zodiac)
        if horoscope_type == HOROSCOPE_ABOUT:
            horoscope_message = MASSAGES_HOROSCOPE_ABOUT[zodiac]['main']
            horoscope_stick = MASSAGES_HOROSCOPE_ABOUT[zodiac]['sticker']
            await bot.send_sticker(chat_id=callback.from_user.id,
                                   sticker=horoscope_stick)
            await callback.message.answer(horoscope_message, reply_markup=button_appendix)

        elif horoscope_type == HOROSCOPE_TODAY or horoscope_type == HOROSCOPE_TOMORROW:
            if horoscope_type == HOROSCOPE_TODAY:
                day = 'today'
            else:
                day = 'tomorrow'
            horoscope = parse_horoscope_for_zodiac(zodiac, day)
            zodiac_str = zodiac.upper()
            zodiac = globals().get(zodiac_str)
            await callback.message.answer(f'{zodiac} {horoscope_type}:\n\n')
            await callback.message.answer(horoscope)

        elif horoscope_type == HOROSCOPE_COMPATIBILITY:
            if horoscope_compatibility_he:
                horoscope = parse_horoscope_compatibility(horoscope_compatibility_he, zodiac)
                zodiac_str = zodiac.upper()
                zodiac = globals().get(zodiac_str)
                horoscope_compatibility_he_str = horoscope_compatibility_he.upper()
                horoscope_compatibility_he = globals().get(horoscope_compatibility_he_str)
                await callback.message.answer(f'{horoscope_type} для: мужчина - {horoscope_compatibility_he} и '
                                              f'девушка {zodiac}:\n\n')
                await state.finish()
                for msg_horoscope in horoscope:
                    await callback.message.answer(msg_horoscope)
            else:
                await state.update_data(horoscope_compatibility_he=zodiac)
                await callback.message.answer(HOROSCOPE_COMPATIBILITY_SHE, reply_markup=znaki_zodiaka_inline)
    except KeyError as e:
        await callback.message.answer(f'Так, {callback.from_user["first_name"]}, то то заходишь, '
                                      f'то выходишь, '
                                      f'я забыла о чем мы горорили. Давай сначала, жми кнопку внизу')
        await state.finish()

# zodiacs
OVEN = '♈️ Овен'
TELEC = '♉️ Телец'
BLIZNECY = '♊️ Близнецы'
RAK = '♋️ Рак'
LEV = '♌️ Лев'
DEVA = '♍️ Дева'
VESY = '♎️ Весы'
SCORPION = '♏️ Скорпион'
STRELEC = '♐️ Стрелец'
KOZEROG = '♑️ Козерог'
VODOLEI = '♒️ Водолей'
RYBY = '♓️ Рыбы'

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
