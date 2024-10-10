from aiogram import types, Router, F, Bot, Dispatcher
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters import ChatTypeFilter
from app.keyboards import intro_kb, add_goal_kb, reset_goal_kb, price_kb, sub_price_kb, select_tarif_kb

user_router = Router()
user_router.message.filter(ChatTypeFilter(["private"]))

previous_bot_message = None
class ProcessState(StatesGroup):
    first_step = State()
    second_step = State()
class AddUser(StatesGroup):
    name = State()
    phone_number = State()
    tarif = State()

    texts = {
        'AddUser:name': 'Введите имя заново:',
        'AddUser:phone_number': 'Введите номер телефона заново:',
        'AddUser:tarif': 'Введите тариф заново:',
    }

@user_router.message(CommandStart())
async def answer(message: types.Message):
    global previous_bot_message

    m = await message.answer(f"Привет, {message.from_user.first_name}! Я Бот студии танцев BlackFlag. Выберите действие:", reply_markup=intro_kb)
    previous_bot_message = m.message_id

# @user_router.callback_query(F.data == "price_list")
# async def price_list(callback_query: types.CallbackQuery, state: FSMContext):
#     global previous_bot_message
#
#     await message.answer('Выберите подходящий тариф', reply_markup=price_kb)



@user_router.callback_query(StateFilter("*"), F.data == "cancel")
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    # await callback_query.message.edit_text("Действие отменено", reply_markup=add_goal_kb)
    await answer(callback_query.message)
    

@user_router.callback_query(StateFilter("*"), F.data == "back")
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    current_state = await state.get_state()

    if current_state == AddUser.name:
        await state.clear()
        # await callback_query.message.edit_text("Действие отменено", reply_markup=add_goal_kb)
        await answer(callback_query.message)
    
    previous_state = await state.get_state()
    for step in AddUser.__all_states__:
        if step.state == current_state:
            await state.set_state(previous_state)
            await callback_query.message.edit_text(f"Вы вернулись к прошлому шагу \n{AddUser.texts[previous_state.state]}", reply_markup=add_goal_kb)
        previous_state = step


@user_router.callback_query(F.data == "book")
async def add_goal(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    await callback_query.message.edit_text("Введите свое имя: ", reply_markup=add_goal_kb)
    await state.set_state(AddUser.name)
@user_router.callback_query(F.data == "price_list")
async def add_goal(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    await callback_query.message.edit_text("Наши тарифы: ", reply_markup=price_kb)

@user_router.callback_query(F.data == "back_to_main")
async def add_goal(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    await callback_query.message.edit_text("Вы вернулись на главную", reply_markup=intro_kb)
@user_router.callback_query(F.data == "abonements")
async def add_goal(callback_query: types.CallbackQuery, state: FSMContext):
    global previous_bot_message

    await callback_query.message.edit_text("Наши абонементы: ", reply_markup=sub_price_kb)

@user_router.message(AddUser.name)
async def add_name(message: types.Message, bot: Bot, state: FSMContext):
    global previous_bot_message

    await state.update_data(name=message.text)
    await message.delete()
    data = await state.get_data()
    await bot.edit_message_text(f"Имя: {data['name']}\n"
                                "Введите номер телефона для связи: ",
                                chat_id=message.chat.id,
                                message_id=previous_bot_message,
                                reply_markup=add_goal_kb)
    await state.set_state(AddUser.phone_number)


@user_router.message(AddUser.phone_number)
async def add_phone_number(message: types.Message, bot: Bot, state: FSMContext):
    global previous_bot_message

    await state.update_data(phone_number=message.text)
    await message.delete()
    data = await state.get_data()
    await bot.edit_message_text(f"Имя: {data['name']}\n"
                                f"Номер телефона: {data['phone_number']}\n"
                                "Выберите подходящий вам тариф(например: Разовое посещение): ",
                                chat_id=message.chat.id,
                                message_id=previous_bot_message,
                                reply_markup=select_tarif_kb)
    await state.set_state(AddUser.tarif)

@user_router.callback_query(F.data.startswith('tarif_'))
async def add_tarif(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext):
    global previous_bot_message
    selected_tarif = callback_query.data.split("_")[1]
    await state.update_data(tarif=selected_tarif)
    data = await state.get_data()
    other_user_chat_id = 6121957414
    #  485061270 me
    # 1271362249 2 me
    # 1271362249
    await bot.send_message(other_user_chat_id,f'Данные из бота:{data["name"]}, {data['phone_number']}, {data['tarif']}\n')
    await state.update_data(first_step='first_step')

@user_router.message(F.data.second_step)
async def add_tarif_message(message: types.Message, bot: Bot, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    await bot.edit_message_text(f"Ваше имя: {data['name']},\n"
                                f"Номер телефона: {data['phone_number']},\n"
                                f"Тариф: {data['tarif']}\n",
                                chat_id=message.chat.id,
                                message_id=previous_bot_message,
                                reply_markup=reset_goal_kb)

    await state.clear()


