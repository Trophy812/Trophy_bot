import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
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


# ====== ГЛАВНОЕ МЕНЮ (inline, 2 столбика) ======
def get_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🗺️ Где купить?", callback_data="main_where"),
                InlineKeyboardButton(text="💳 Как платить?", callback_data="main_pay")
            ],
            [
                InlineKeyboardButton(text="📦 Когда получить?", callback_data="main_when"),
                InlineKeyboardButton(text="📞 Зови Степаныча", callback_data="main_call")
            ]
        ]
    )


# ====== БЛОК 2: INLINE‑КНОПКИ (2 столбика) ======
def get_block2_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚗 Купить с колес", callback_data="lead1"),
                InlineKeyboardButton(text="📞 Зови Степаныча", callback_data="lead2")
            ],
            [
                InlineKeyboardButton(text="📱 Авито", url="https://www.avito.ru/brands/4x4spb/all?gdlkerfdnwq=101&page_from=from_item_card&iid=7841359262&sellerId=3288992683cf68e0f0a42a16a71c4103"),
                InlineKeyboardButton(text="🌐 Сайт", url="https://4x4spb.ru/")
            ],
            [
                InlineKeyboardButton(text="📍 Где магазин", url="https://yandex.ru/maps/-/CPQcV6JZ"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")
            ]
        ]
    )


def get_block3_menu():
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


# ====== ОБРАБОТЧИКИ INLINE‑КНОПОК ГЛАВНОГО МЕНЮ ======
@dp.callback_query(F.data == "main_where")
async def main_where_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.block2)
    await callback.message.edit_text(
        text="""Где мы продаем? Хм, везде.

💡 Если ты живешь в Санкт-Петербурге, то легче всего купить через менеджера по звонку.
💡 Или приехать в магазин.
💡 Если в другом городе, то через Авито
💡 Третий вариант - через сайт, но имейте ввиду, что на сайт попадает не весь ассортимент, некоторые позиции уходят прямо с колес""",
        reply_markup=get_block2_menu()
    )
    await callback.answer()


@dp.callback_query(F.data == "main_pay")
async def main_pay_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.block3)
    await callback.message.edit_text(
        text="""Магазин работает со всеми вариантами оплаты:

💰 Наличные в магазине
💳 Платеж по карте в магазине
📱 QR код (СБП)
💻 Безопасная сделка на Авито
🧾 Безналичный расчет для юридических лиц по счету, с НДС""",
        reply_markup=get_block3_menu()
    )
    await callback.answer()


@dp.callback_query(F.data == "main_when")
async def main_when_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.block4)
    await callback.message.edit_text(
        text="""📆 Отправим в день оплаты.

📅 САМОВЫВОЗ: из магазина в Санкт-Петербурге на Мгинской 7 с понедельника по пятницу, 11.00 - 19.00

🚙 ДОСТАВКА в Санкт-Петербурге: везем сами по согласованию с покупателем.

🚚 ДОСТАВКА за пределы Санкт-Петербурга. Любой транспортной компанией: Деловые линии, Энергия, КИТ, ПЭК, СДЭК, Авито доставка.""",
        reply_markup=get_block4_menu()
    )
    await callback.answer()


@dp.callback_query(F.data == "main_call")
async def main_call_callback(callback: types.CallbackQuery, state: FSMContext):
    # Пока заглушка, потом заменим на блок сбора данных
    await callback.message.edit_text("📞 Соединяю с кожаным Степанычем!\n(Блок сбора данных — добавим позже)")
    await callback.answer()


# ====== ОБРАБОТЧИКИ INLINE‑КНОПОК БЛОКОВ 2–4 ======
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
    # Возвращаем главное меню (тоже inline)
    await callback.message.edit_text(
        text="Что тебе рассказать?",
        reply_markup=get_main_menu()
    )
    await state.set_state(BotStates.main_menu)
    await callback.answer()


# ====== БЛОКИРОВКА ЛЮБЫХ ТЕКСТОВЫХ СООБЩЕНИЙ ======
@dp.message()
async def block_all_text(message: types.Message):
    # Игнорируем всё, что не является командой /start
    pass


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())