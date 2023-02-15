from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    horoscope_type = State()
    horoscope_for = State()
    zodiac = State()
    horoscope_compatibility_he = State()
    horoscope_compatibility_she = State()
