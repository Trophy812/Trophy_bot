import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
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

# ====== ГЛАВНОЕ МЕНЮ (Блок 1) ======
def get_main_menu():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🗺️ Где купить?")],
        [KeyboardButton(text="💳 Как платить?")],
        [KeyboardButton(text="📦 Когда и как получить?")],
        [KeyboardButton(text="📞 Зови кожаного Степаныча")]
    ], resize_keyboard=True)
    return kb

@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    text = """Привет! Я помощник Степаныча, знаю все про магазин 4x4spb.ru/

Что тебе рассказать?"""
    # Место для картинки: await message.answer_photo("URL_КАРТИНКИ", caption=text, reply_markup=get_main_menu())
    await message.answer(text, reply_markup=get_main_menu())
    await state.set_state(BotStates.main_menu)

# ====== БЛОК 2: Где купить? ======
def get_block2_menu():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🚗 Хочу купить 'с колес'")],
        [KeyboardButton(text="📞 Зови кожаного Степаныча")],
        [KeyboardButton(text="📱 Авито")],
        [KeyboardButton(text="🌐 Сайт")],
        [KeyboardButton(text="📍 Узнать, где магазин")],
        [KeyboardButton(text="🔙 Назад")]
    ], resize_keyboard=True)
    return kb

@dp.message(BotStates.main_menu, F.text == "🗺️ Где купить?")
async def block2_handler(message: types.Message):
    text = """Где мы продаем? Хм, везде.

💡 Если ты живешь в Санкт-Петербурге, то легче всего купить через менеджера по звонку.
💡 Или приехать в магазин.
💡 Если в другом городе, то через Авито
💡 Третий вариант - через сайт, но имейте ввиду, что на сайт попадает не весь ассортимент, некоторые позиции уходят прямо с колес"""
    await message.answer(text, reply_markup=get_block2_menu())

@dp.message(F.text == "🚗 Хочу купить 'с колес'")
async def block2_lead1(message: types.Message):
    # ПЕРЕХОД НА БЛОК "СБОР ДАННЫХ" - добавим позже
    await message.answer("📞 Соединяю с кожаным Степанычем!")

@dp.message(F.text == "📞 Зови кожаного Степаныча")
async def block2_lead2(message: types.Message):
    # ПЕРЕХОД НА БЛОК "СБОР ДАННЫХ" - добавим позже
    await message.answer("📞 Соединяю с кожаным Степанычем!")

@dp.message(F.text == "📱 Авито")
async def block2_avito(message: types.Message):
    # ВСТАВЬТЕ ССЫЛКУ НА АВИТО
    await message.answer("🔗 https://avito.ru/your_link\n\nИли нажмите кнопку ниже:", 
                        reply_markup=get_block2_menu())

@dp.message(F.text == "🌐 Сайт")
async def block2_site(message: types.Message):
    # ВСТАВЬТЕ ССЫЛКУ НА САЙТ
    await message.answer("🔗 https://4x4spb.ru/\n\nИли нажмите кнопку ниже:", 
                        reply_markup=get_block2_menu())

@dp.message(F.text == "📍 Узнать, где магазин")
async def block2_map(message: types.Message):
    # ВСТАВЬТЕ ССЫЛКУ НА ЯНДЕКС.КАРТЫ
    await message.answer("📍 https://yandex.ru/maps/?text=Мгинская+7+Санкт-Петербург\n\nМагазин на Мгинской 7", 
                        reply_markup=get_block2_menu())

# ====== БЛОК 3: Как платить? ======
def get_block3_menu():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🔙 Назад")]
    ], resize_keyboard=True)
    return kb

@dp.message(BotStates.main_menu, F.text == "💳 Как платить?")
async def block3_handler(message: types.Message):
    text = """Магазин работает со всеми вариантами оплаты:

💰 Наличные в магазине
💳 Платеж по карте в магазине
📱 QR код (СБП)
💻 Безопасная сделка на Авито
🧾 Безналичный расчет для юридических лиц по счету, с НДС"""
    await message.answer(text, reply_markup=get_block3_menu())

# ====== БЛОК 4: Доставка ======
def get_block4_menu():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🔙 Назад")]
    ], resize_keyboard=True)
    return kb

@dp.message(BotStates.main_menu, F.text == "📦 Когда и как получить?")
async def block4_handler(message: types.Message):
    text = """📆 Отправим в день оплаты.

📅 Для самовывоза магазин в Санкт-Петербурге на Мгинской 7 работает с понедельника по пятницу, 11.00 - 19.00

🚙 В пределах Санкт-Петербурга - везем сами по согласованию.

🚚 За пределы Санкт-Петербурга доставим любой транспортной компанией: Деловые линии, Энергия, КИТ, ПЭК, СДЭК, Авито доставка."""
    await message.answer(text, reply_markup=get_block4_menu())

# ====== НАЗАД В ГЛАВНОЕ МЕНЮ ======
@dp.message(F.text == "🔙 Назад")
async def back_to_main(message: types.Message, state: FSMContext):
    text = "Что тебе рассказать?"
    await message.answer(text, reply_markup=get_main_menu())
    await state.set_state(BotStates.main_menu)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
