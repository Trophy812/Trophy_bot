import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove
)
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


# ====== ГЛАВНОЕ МЕНЮ (ReplyKeyboard, 2 колонки) ======
def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗺️ Где купить?"), KeyboardButton(text="💳 Как платить?")],
            [KeyboardButton(text="📦 Когда получить?"), KeyboardButton(text="📞 Зови Степаныча")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


# ====== БЛОК 2: INLINE‑КНОПКИ (2 столбика) ======
def get_block2_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # Первая строка — две кнопки
            [
                InlineKeyboardButton(text="🚗 Купить с колес", callback_data="lead1"),
                InlineKeyboardButton(text="📞 Зови Степаныча", callback_data="lead2")
            ],
            # Вторая строка — две кнопки
            [
                InlineKeyboardButton(text="📱 Авито", url="https://www.avito.ru/brands/4x4spb/all?gdlkerfdnwq=101&page_from=from_item_card&iid=7841359262&sellerId=3288992683cf68e0f0a42a16a71c4103"),
                InlineKeyboardButton(text="🌐 Сайт", url="https://4x4spb.ru/")
            ],
            # Третья строка — две кнопки
            [
                InlineKeyboardButton(text="📍 Где магазин", url="https://yandex.ru/maps/-/CPQcV6JZ"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")
            ]
        ]
    )


def get_block3_menu():
    # Только одна кнопка — оставляем как есть
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
        ]
    )


def get_block4_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
        ]
    )


# ====== СТАРТ ======
@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    text = """Привет! Я помощник Степаныча, знаю все про магазин 4x4spb.ru/

Что тебе рассказать?"""
    await message.answer(text, reply_markup=get_main_menu())
    await state.set_state(BotStates.main_menu)


# ====== ПЕРЕХОДЫ ИЗ ГЛАВНОГО МЕНЮ (убираем Reply‑клавиатуру) ======
@dp.message(StateFilter(BotStates.main_menu), F.text == "🗺️ Где купить?")
async def block2_handler(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.block2)
    # Убираем основную клавиатуру
    await message.answer("⚙️ Загружаю информацию...", reply_markup=ReplyKeyboardRemove())
    text = """Где мы продаем? Хм, везде.

💡 Если ты живешь в Санкт-Петербурге, то легче всего купить через менеджера по звонку.
💡 Или приехать в магазин.
💡 Если в другом городе, то через Авито
💡 Третий вариант - через сайт, но имейте ввиду, что на сайт попадает не весь ассортимент, некоторые позиции уходят прямо с колес"""
    await message.answer(text, reply_markup=get_block2_menu())


@dp.message(StateFilter(BotStates.main_menu), F.text == "💳 Как платить?")
async def block3_handler(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.block3)
    await message.answer("⚙️ Загружаю информацию...", reply_markup=ReplyKeyboardRemove())
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
    await message.answer("⚙️ Загружаю информацию...", reply_markup=ReplyKeyboardRemove())
    text = """📆 Отправим в день оплаты.

📅 Для самовывоза магазин в Санкт-Петербурге на Мгинской 7 работает с понедельника по пятницу, 11.00 - 19.00

🚙 В пределах Санкт-Петербурга - везем сами по согласованию.

🚚 За пределы Санкт-Петербурга доставим любой транспортной компанией: Деловые линии, Энергия, КИТ, ПЭК, СДЭК, Авито доставка."""
    await message.answer(text, reply_markup=get_block4_menu())


@dp.message(StateFilter(BotStates.main_menu), F.text == "📞 Зови Степаныча")
async def main_lead(message: types.Message):
    # Пока заглушка, потом заменим на полноценный блок сбора данных
    await message.answer("📞 Соединяю с кожаным Степанычем!\n(Блок сбора данных — добавим позже)")


# ====== ОБРАБОТЧИКИ INLINE‑КНОПОК ======
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
    # Удаляем сообщение с инлайн‑кнопками, чтобы не загромождать чат
    await callback.message.delete()
    # Отправляем новое сообщение с главным меню и Reply‑клавиатурой
    await callback.message.answer(
        "Что тебе рассказать?",
        reply_markup=get_main_menu()
    )
    await state.set_state(BotStates.main_menu)
    await callback.answer()


# ====== БЛОКИРОВКА ЛЮБЫХ ТЕКСТОВЫХ СООБЩЕНИЙ ======
@dp.message()
async def block_all_text(message: types.Message):
    # Игнорируем любые сообщения, которые не обработаны выше
    pass


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())