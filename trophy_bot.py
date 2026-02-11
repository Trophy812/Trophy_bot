import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class BotStates(StatesGroup):
    main_menu = State()
    block2 = State()
    block3 = State()
    block4 = State()

# ====== ГЛАВНОЕ МЕНЮ (ОСТАЕТСЯ ReplyKeyboard) ======
def get_main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🗺️ Где купить?"), KeyboardButton(text="💳 Как платить?")],
        [KeyboardButton(text="📦 Когда получить?"), KeyboardButton(text="📞 Зови Степаныча")]
    ], resize_keyboard=True, one_time_keyboard=False)

# ====== БЛОК 2: INLINE-КНОПКИ С ССЫЛКАМИ ======
def get_block2_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Купить с колес", callback_data="lead1")],
        [InlineKeyboardButton(text="📞 Зови Степаныча", callback_data="lead2")],
        [InlineKeyboardButton(text="📱 Авито", url="https://www.avito.ru/brands/4x4spb/all?gdlkerfdnwq=101&page_from=from_item_card&iid=7841359262&sellerId=3288992683cf68e0f0a42a16a71c4103")],
        [InlineKeyboardButton(text="🌐 Сайт", url="https://4x4spb.ru/")],
        [InlineKeyboardButton(text="📍 Где магазин", url="https://yandex.ru/maps/-/CPQcV6JZ")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
    ])

def get_block3_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
    ])

def get_block4_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
    ])

# ====== ОБРАБОТЧИКИ ======
@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    text = """Привет! Я помощник Степаныча, знаю все про магазин 4x4spb.ru/

Что тебе рассказать?"""
    await message.answer(text, reply_markup=get_main_menu())
    await state.set_state(BotStates.main_menu)

@dp.message(StateFilter(BotStates.main_menu), F.text == "🗺️ Где купить?")
async def block2_handler(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.block2)
    text = """Где мы продаем? Хм, везде.

💡 Если ты живешь в Санкт-Петербурге, то легче всего купить через менеджера по звонку.
💡 Или приехать в магазин.
💡 Если в другом городе, то через Авито
💡 Третий вариант - через сайт, но имейте ввиду, что на сайт попадает не весь ассортимент, некоторые позиции уходят прямо с колес"""
    await message.answer(text, reply_markup=get_block2_menu())

@dp.message(StateFilter(BotStates.main_menu), F.text == "💳 Как платить?")
async def block3_handler(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.block3)
    text = """Магазин работает со всеми вариантами оплаты:

💰 Наличные в магазине
💳 Платеж по карте в магазине
📱 QR код (СБП)
💻 Безопасная сделка на Авито
🧾 Безналичный расчет для юридических лиц по счету, с НДС"""
    await message.answer(text, reply_markup=get_block3_menu())

@dp.message(StateFilter(BotStates.main_menu), F.text == "📦 Когда получить?")
async def block4_handler(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.block4)
    text = """📆 Отправим в день оплаты.

📅 Для самовывоза магазин в Санкт-Петербурге на Мгинской 7 работает с понедельника по пятницу, 11.00 - 19.00

🚙 В пределах Санкт-Петербурга - везем сами по согласованию.

🚚 За пределы Санкт-Петербурга доставим любой транспортной компанией: Деловые линии, Энергия, КИТ, ПЭК, СДЭК, Авито доставка."""
    await message.answer(text, reply_markup=get_block4_menu())

@dp.message(StateFilter(BotStates.main_menu), F.text == "📞 Зови Степаныча")
async def main_lead(message: types.Message):
    await message.answer("📞 Соединяю с кожаным Степанычем!\n(Блок сбора данных — добавим позже)")

# ====== CALLBACK ОБРАБОТЧИКИ (ДЛЯ INLINE-КНОПОК) ======
@dp.callback_query(F.data == "lead1")
async def callback_lead1(callback: types.CallbackQuery):
    await callback.message.edit_text("📞 Соединяю с кожаным Степанычем!\n(Блок сбора данных)")
    await callback.answer()

@dp.callback_query(F.data == "lead2")
async def callback_lead2(callback: types.CallbackQuery):
    await callback.message.edit_text("📞 Соединяю с кожаным Степанычем!\n(Блок сбора данных)")
    await callback.answer()

@dp.callback_query(F.data == "back_main")
async def callback_back_main(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.main_menu)
    await callback.message.edit_text("Что тебе рассказать?", reply_markup=get_main_menu())
    await callback.answer()

# ====== БЛОКИРОВКА ======
@dp.message()
async def block_all_text(message: types.Message):
    pass

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
