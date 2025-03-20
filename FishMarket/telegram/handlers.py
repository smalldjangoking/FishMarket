from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram import F
from checkout.models import Order
from telegram.helpers import get_orders_queryset, prepare_order_message_and_keyboard, get_order_by_id, \
    get_kb_from_order, get_orders_queryset_all

router = Router()

#main keyboard
main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обработка 📝'), KeyboardButton(text='Отправленные 📦')],
    [KeyboardButton(text='Поиск Заказа 🔍')],
], resize_keyboard=True, input_field_placeholder='Воспользуйтесь меню')

#cancel button
cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Завершить ⬅️")]],
    resize_keyboard=True,
    input_field_placeholder="Введите номер заказа или нажмите Завершить"
)

#state for searching item
class OrderSearch(StatesGroup):
    waiting_for_order_input = State()


#/start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('🚀 Добро пожаловать в быстрый обработчик заказов! \n\n\n'
                         '✅ Вы будете автоматически получать уведомления о новых заказах.\n'
                         '⚙️ Также вы можете управлять заказами через меню.\n\n'
                         '❗️ Заказы, которые отмечены как "Завершены" или "Отменены", не будут отображаться в боте.', reply_markup=main)


#handler for search 🔍
@router.message(lambda message: message.text == "Поиск Заказа 🔍")
async def search_order(message: Message, state: FSMContext):
    await message.answer("Введите номер заказа или телефон получателя ✍️", reply_markup=cancel_kb)
    await state.set_state(OrderSearch.waiting_for_order_input)



@router.message(OrderSearch.waiting_for_order_input, F.text == "Завершить ⬅️")
async def cancel_search(message: Message, state: FSMContext):
    await message.answer("Поиск завершен.", reply_markup=main)
    await state.clear()


@router.message(OrderSearch.waiting_for_order_input)
async def process_order_search(message: Message, state: FSMContext):
    search_input = message.text

    orders = await get_orders_queryset(search_input)

    if orders:
        for order in orders:
            text, kb = prepare_order_message_and_keyboard(order)
            await message.answer(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    else:
        await message.answer(
            f'Заказы не обнаружены с запросом {search_input}. Попробуйте другой запрос или нажмите "Завершить"',
            reply_markup=cancel_kb)

    await state.set_state(OrderSearch.waiting_for_order_input)
    await message.answer(f'Продолжим поиск? 🕵️‍♂️ или нажмите кнопку "Завершить ⬅️"', reply_markup=cancel_kb)


@router.message((F.text == "Обработка 📝") | (F.text == "Отправленные 📦"))
async def all_orders(message: Message):
    status_map = {
        "Обработка 📝": 1,
        "Отправленные 📦": 2
    }

    status_id = status_map.get(message.text)
    orders = await get_orders_queryset_all(status_id)

    if orders:
        for order in orders:
            text, kb = prepare_order_message_and_keyboard(order)
            await message.answer(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    else:
        await message.answer(f"Заказы со статусом '{message.text}' не найдены.")


@router.callback_query(F.data.startswith('order_') & F.data.endswith('is_paid'))
async def set_order_paid(callback: CallbackQuery):
    order_id = callback.data.split("_")[1]
    await Order.objects.filter(id=order_id).aupdate(is_paid=True)

    order = await get_order_by_id(order_id)
    text, kb = prepare_order_message_and_keyboard(order)

    await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")


@router.callback_query(F.data.startswith('order_') & F.data.endswith('status'))
async def status_for_order(callback: CallbackQuery):
    order_id = callback.data.split("_")[1]
    status_id = callback.data.split("_")[2]

    kb = get_kb_from_order(order_id, status_id)

    await callback.message.edit_reply_markup(reply_markup=kb.as_markup())
    await callback.answer()


@router.callback_query(F.data.startswith('set_status') & F.data.endswith('status_label'))
async def set_status_for_order(callback: CallbackQuery):
    order_id = callback.data.split("_")[2]
    status_id = callback.data.split("_")[4]
    await Order.objects.filter(id=order_id).aupdate(status=status_id)

    if int(status_id) not in [3, 4]:
        order = await get_order_by_id(order_id)
        text, kb = prepare_order_message_and_keyboard(order)
        await callback.message.edit_text(text, reply_markup=kb.as_markup(), parse_mode="HTML")
    else:
        await callback.message.delete()


@router.callback_query(F.data.startswith('set_status_') & F.data.endswith('status_exit'))
async def set_order_paid(callback: CallbackQuery):
    order_id = callback.data.split("_")[2]

    order = await get_order_by_id(order_id)
    text, kb = prepare_order_message_and_keyboard(order)

    await callback.message.edit_reply_markup(reply_markup=kb.as_markup())