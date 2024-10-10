from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


intro_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='Записаться на занятие', callback_data='book'),
                InlineKeyboardButton(text='Прайс лист', callback_data='price_list')
            ]
        ]
)

add_goal_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='Отменить', callback_data='cancel'),
                InlineKeyboardButton(text='Назад', callback_data='back'),
            ]
        ]
)

reset_goal_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='Готово!✅ С вами свяжется наш менеджер, хорошего дня!', callback_data='price_list'),
            ]
        ]
)
price_kb = InlineKeyboardMarkup(
    inline_keyboard=[
                [InlineKeyboardButton(text='Разовое занятие  - 800₽', callback_data='tarif_1')],
                [InlineKeyboardButton(text='Первое пробное  - 600₽', callback_data='tarif_2')],
                [InlineKeyboardButton(text='Абонементы', callback_data='abonements')],
                [InlineKeyboardButton(text='Записаться на занятие', callback_data='book')],
                [InlineKeyboardButton(text='Назад', callback_data='back_to_main')],
    ]
)
sub_price_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='4 занятия - 2700₽', callback_data='tarif_abon1'),],
        [InlineKeyboardButton(text='8 занятий - 5000₽', callback_data='tarif_abon2'),],
        [InlineKeyboardButton(text='12 занятий - 6900₽', callback_data='tarif_abon3')],
        [InlineKeyboardButton(text='Записаться на занятие', callback_data='book')],
        [InlineKeyboardButton(text='Назад', callback_data='back_to_main')]
    ]
)
select_tarif_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Разовое занятие  - 800₽', callback_data='tarif_1'),],
        [InlineKeyboardButton(text='Первое пробное  - 600₽', callback_data='tarif_1'),],
        [InlineKeyboardButton(text='Абонементы', callback_data='abonements')],
        [InlineKeyboardButton(text='Назад', callback_data='back_to_main')]
    ]
)