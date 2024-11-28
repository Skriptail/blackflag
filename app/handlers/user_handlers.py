import json

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile

from filters import ChatTypeFilter
from keyboards import (
    back_to_main_kb,
    intro_kb,
    tarif_selection_kb,
    after_tarif_kb
)

user_router = Router()
user_router.message.filter(ChatTypeFilter(["private"]))

class AddUser(StatesGroup):
    name = State()
    phone_number = State()
    tarif = State()
    last_message = State()

    texts = {
        'AddUser:name': 'Введите имя заново:',
        'AddUser:phone_number': 'Введите номер телефона заново:',
        'AddUser:number_of_table': 'Введите тариф заново:',
    }
@user_router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    sent_message = await message.answer(
        f"Привет, {message.from_user.first_name}! Я Бот студии танцев BlackFlag.🏴\n"
        "Для навигации используйте кнопки ниже",
        reply_markup=intro_kb)
    await state.update_data(last_message=sent_message.message_id)

@user_router.callback_query(F.data == "book")
async def add_goal(callback_query: types.CallbackQuery, state: FSMContext):
    sent_message = await callback_query.message.edit_text("Давайте познакомимся и запишемся на занятие! Введите, пожалуйста, свое имя: ", reply_markup=back_to_main_kb)
    await state.update_data(last_message_id=sent_message.message_id) 
    await state.set_state(AddUser.name)

@user_router.callback_query(F.data == "back_to_main")
async def add_goal(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    # last_message_id = data.get('last_message_id')
    # if last_message_id:
    #     await bot.delete_message(callback_query.message.chat.id, message_id=last_message_id)
    await callback_query.message.edit_text("Вы вернулись на главную", reply_markup=intro_kb)
    await state.clear()

@user_router.message(AddUser.name)
async def add_phone_number(message: types.Message, state: FSMContext, bot: Bot):
    await state.update_data(name=message.text)
    await message.delete()
    data = await state.get_data()
    last_message_id = data.get('last_message_id')

    await bot.edit_message_text(f"Имя: {data['name']}\n"
                                "Введите номер телефона: ",
                                chat_id=message.chat.id,
                                message_id=last_message_id,
                                reply_markup=back_to_main_kb)
    await state.set_state(AddUser.phone_number)

@user_router.message(AddUser.phone_number)
async def add_tarif(message: types.Message, bot: Bot, state: FSMContext):

    await state.update_data(phone_number=message.text)
    await message.delete()
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    await bot.edit_message_text(f"Имя: {data['name']}\n"
                                f"Номер телефона: {data['phone_number']}\n"
                                "Выберите подходящий тариф: ",
                                chat_id=message.chat.id,
                                message_id=last_message_id,
                                reply_markup=tarif_selection_kb)
    await state.set_state(AddUser.tarif)

@user_router.callback_query(F.data.startswith('tarif'))
async def add_number_of_table(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    selected_number_of_table = callback_query.data.split("_")[1]
    await state.update_data(tarif=selected_number_of_table)
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    await bot.edit_message_text(f"Ваше имя: {data['name']}\n"
        f"Номер телефона: {data['phone_number']}\n"
        f"Выбранный тариф: {data['tarif']}\n",
        chat_id=callback_query.message.chat.id,
        message_id=last_message_id,
        reply_markup=after_tarif_kb)
    other_user_chat_id = 485061270
    await bot.send_message(
        other_user_chat_id,
        'Данные из бота:\n'
        f'Имя: {data["name"]}\n'
        f'Выбранный тариф: {data["tarif"]}\n'
        f'Номер телефона: {data["phone_number"]}\n')

@user_router.callback_query(F.data == "masters")
async def masters(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    await callback_query.message.edit_text('Наши педагоги\n'
                           'Татьяна Седых - Расписание курсов: Вторник/Четверг 21:00\n'
                           'Хлебникова Анастасия -  jazz funk, choreo', reply_markup=back_to_main_kb)

@user_router.callback_query(F.data == "price")
async def price(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    await callback_query.message.edit_text('Наш прайс лист:\n'
                           'Разовое занятие - 800₽\n'
                           'Первое пробное - 600₽\n'
                           '<b>Абонементы</b>\n'
                           '<i>Скидка на первый абонемент в течение 3-х дней после пробного занятия</i>\n'
                           '<i>Цена со звездочкой указана с учетом скидки</i>\n'
                           '4 занятия - 2700₽ (2150₽*)\n'
                           '8 занятий - 5000₽ (4000₽*)\n'
                           '12 занятий - 6900₽ (5500₽*)\n',  reply_markup=back_to_main_kb, parse_mode='HTML')

@user_router.callback_query(F.data == "rent")
async def rent(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback_query.message.edit_text('<b>140кв.м</b>, две раздевалки\n'
                                           'Высота потолков - 4м\n'
                                           'Покрытие - линолеум\n'
                                           'Окна с рулонными шторами\n'
                                           'Звук - колонки\n'
                                           'Воздух - два кондиционера\n'
                                           'А также дополнительное освещение для ваших съемок\n'
                                           '<i>Малышева 28</i>',  reply_markup=back_to_main_kb, parse_mode='HTML')

@user_router.callback_query(F.data == "help")
async def help(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback_query.message.edit_text('<b>Помощь по навигации в боте</b>\n'
                                           'https://vk.link/blackflagekb - группа Вконтакте\n'
                                           '89518013886 - номер поддержки',  reply_markup=back_to_main_kb, parse_mode='HTML')
