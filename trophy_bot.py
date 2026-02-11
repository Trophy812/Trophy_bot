import asyncio
import os
from aiogram import Bot, Dispatcher, types, F, filters  # Добавил filters сюда
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Токен из переменной окружения
API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Состояния для отслеживания блоков
class BotStates(StatesGroup):
    main_menu = State()
    block2 = State()
    block3 = State()
    block4 = State()

# ====== ГЛАВНОЕ МЕНЮ (Блок 1) - 2 столбика ======
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

# ====== БЛОК 2 ======
@dp.message(StateFilter(BotStates.block2), F.text == "🚗 Купить с колес")
async def block2_lead1(message: types.Message):
    await message.answer("📞 Соединяю с кожаным Степанычем!\n(Блок сбора данных)")

@dp.message(StateFilter(BotStates.block2), F.text == "📞 Зови Степаныча")
async def block2_lead2(message: types.Message):
    await message.answer("📞 Соединяю с кожаным Степанычем!\n(Блок сбора данных)")

@dp.message(StateFilter(BotStates.block2), F.text == "📱 Авито")
async def block2_avito(message: types.Message):
    await message.answer("🔗 https://www.avito.ru/user/3288992683cf68e0f0a42a16a71c4103/profile/all?id=7905720699&src=item&sellerId=3288992683cf68e0f0a42a16a71c4103", reply_markup=get_block2_menu())

@dp.message(StateFilter(BotStates.block2), F.text == "🌐 Сайт")
async def block2_site(message: types.Message):
    await message.answer("🔗 https://4x4spb.ru/", reply_markup=get_block2_menu())

@dp.message(StateFilter(BotStates.block2), F.text == "📍 Где магазин")
async def block2_map(message: types.Message):
    await message.answer("📍 https://yandex.ru/maps/-/CPQcV6JZ", reply_markup=get_block2_menu())

# ====== НАЗАД ======
@dp.message(F.text == "🔙 Назад")
async def back_to_main(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.main_menu)
    await message.answer("Что тебе рассказать?", reply_markup=get_main_menu())

# ====== ПОЛНАЯ БЛОКИРОВКА ВСЕГО ОСТАЛЬНОГО ======
@dp.message()
async def block_all_text(message: types.Message):
    # НИЧЕГО НЕ ОТВЕЧАЕТ на любой свободный текст
    pass

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
