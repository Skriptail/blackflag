from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

intro_kb = InlineKeyboardMarkup(
    inline_keyboard=[
                [InlineKeyboardButton(text='Записаться на занятие', callback_data='book')],
                [InlineKeyboardButton(text='Педагоги', callback_data='masters')],
                [InlineKeyboardButton(text='Цены', callback_data='price')],
                [InlineKeyboardButton(text='Аренда зала', callback_data='rent')],
                [InlineKeyboardButton(text='Помощь', callback_data='help')],

    ]
)
back_to_main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
                [InlineKeyboardButton(text='Назад на главную', callback_data='back_to_main')],
    ]
)
after_tarif_kb = InlineKeyboardMarkup(
    inline_keyboard=[
                [InlineKeyboardButton(text='Готово! С вами свяжутся, чтобы подтвердить запись', callback_data='back_to_main'),
                InlineKeyboardButton(text='', callback_data='null')],
    ]
)
tarif_selection_kb = InlineKeyboardMarkup(
    inline_keyboard=[
                [InlineKeyboardButton(text='Назад на главную', callback_data='back_to_main')],
                [InlineKeyboardButton(text='Разовое занятие - 800₽', callback_data='tarif_one_time')],
                [InlineKeyboardButton(text='Первое пробное - 600₽', callback_data='tarif_first_try')],
                [InlineKeyboardButton(text='4 занятия - 2700₽', callback_data='tarif_4trains')],
                [InlineKeyboardButton(text='8 занятий - 5000₽', callback_data='tarif_8trains')],
                [InlineKeyboardButton(text='12 занятий - 6900₽', callback_data='tarif_12trains')],
    ]
)
