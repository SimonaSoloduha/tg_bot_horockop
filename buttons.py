# Переход на для всех / для одного
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from main import RYBY, OVEN, TELEC, BLIZNECY, RAK, LEV, DEVA, VESY, SCORPION, STRELEC, KOZEROG, VODOLEI
from messages import HOROSCOPE_FOR_ALL, HOROSCOPE_FOR_ONE, HOROSCOPE_ABOUT_APPENDIX, HOROSCOPE_COMPATIBILITY_YES

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

to_day_inline = InlineKeyboardMarkup(row_width=2)
button_for_one = InlineKeyboardButton(text='давай для всех', callback_data=HOROSCOPE_FOR_ALL)
button_for_all = InlineKeyboardButton(text='та для одного', callback_data=HOROSCOPE_FOR_ONE)
to_day_inline.add(button_for_one, button_for_all)

# Переход на характеристику
button_yes = InlineKeyboardMarkup(row_width=1)
button_for_yes = InlineKeyboardButton(text='Да...)', callback_data=HOROSCOPE_FOR_ONE)
button_yes.add(button_for_yes)

# Узнать больше
button_appendix = InlineKeyboardMarkup(row_width=1)
appendix = InlineKeyboardButton(text='Расскажи что еще знаешь', callback_data=HOROSCOPE_ABOUT_APPENDIX)
button_appendix.add(appendix)

# button_yes_no = InlineKeyboardMarkup(row_width=1)
# button_for_yes = InlineKeyboardButton(text='Да...)', callback_data=HOROSCOPE_FOR_ONE)

# Переход на совместимость
button_compatibility = InlineKeyboardMarkup(row_width=1)
button_love_yes = InlineKeyboardButton(text='Угу...)', callback_data=HOROSCOPE_COMPATIBILITY_YES)
button_love_no = InlineKeyboardButton(text='Та не...)', callback_data=HOROSCOPE_COMPATIBILITY_YES)
button_compatibility.add(button_love_yes, button_love_no)

# Выбор знака
znaki_zodiaka_inline = InlineKeyboardMarkup(row_width=3, resize_keyboard=True, )
oven = InlineKeyboardButton(text=OVEN, callback_data='znak_oven')
telec = InlineKeyboardButton(text=TELEC, callback_data='znak_telec')
bliznecy = InlineKeyboardButton(text=BLIZNECY, callback_data='znak_bliznecy')
rak = InlineKeyboardButton(text=RAK, callback_data='znak_rak')
lev = InlineKeyboardButton(text=LEV, callback_data='znak_lev')
deva = InlineKeyboardButton(text=DEVA, callback_data='znak_deva')
vesy = InlineKeyboardButton(text=VESY, callback_data='znak_vesy')
scorpion = InlineKeyboardButton(text=SCORPION, callback_data='znak_scorpion')
strelec = InlineKeyboardButton(text=STRELEC, callback_data='znak_strelec')
kozerog = InlineKeyboardButton(text=KOZEROG, callback_data='znak_kozerog')
vodolei = InlineKeyboardButton(text=VODOLEI, callback_data='znak_vodolei')
ryby = InlineKeyboardButton(text=RYBY, callback_data='znak_ryby')
znaki_zodiaka_inline.add(oven, telec, bliznecy, rak, lev, deva, vesy, scorpion, strelec, kozerog, vodolei, ryby)
