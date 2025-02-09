import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import MessageNotModified
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
import requests
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Настройки логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bot')

# Токены
API_TOKEN = '7711624063:AAH-Ak4OhAoYDeKbQb43tW-qNtKEz6G_B-8'
CRYPTOBOT_API_TOKEN = '324481:AARrPUiiThCGEN5HlHZ9jYUSBwNATb7sLzS'

# Инициализация бота и диспетчера
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

class MenuState(StatesGroup):
    main_menu = State()

# Обработчик команды /start
@dp.message_handler(commands=['start'], state="*")
async def start_command(message: types.Message, state: FSMContext):
    await bot.send_video_note(message.chat.id, video_note=open('C:/Users/fedor/Downloads/Telegram Desktop/диана.mp4', 'rb'))
    welcome_text = (
        "Добро пожаловать в мир страсти и откровенности! 💋\n\n"
        "Меня зовут Диана, и я с радостью приглашаю тебя в закрытый эксклюзивный канал с эротикой🌹\n\n"
        "В моем эксклюзивном канале тебя ждут:\n\n"
        "✨Уникальные кружочки\n"
        "🎧Мои личные аудио\n"
        "📖 Откровенные истории из моей жизни\n"
        "📸 Эротические фотографии и видео\n"
        "✉️Так же сексуальные танцы и стриптиз\n\n"
        "Здесь ты сможешь полностью расслабиться и насладиться общением со мной💞\n\n"
        "Давай исследовать мир удовольствия вместе! ❤️\n\n"
        "Забудь обо всём на свете — я жду тебя. ✨"
    )
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="💵Оплатить доступ", callback_data='pay_access')
    )
    keyboard.add(
        InlineKeyboardButton(text="🍓Больше о приватном канале", callback_data='more_about_private_channel')
    )
    keyboard.add(
        InlineKeyboardButton(text="👤Поддержка", url='https://t.me/your_support_bot')
    )
    await message.answer(welcome_text, reply_markup=keyboard)
    await MenuState.main_menu.set()

# Обработчик нажатий на кнопку "Оплатить доступ"
@dp.callback_query_handler(lambda c: c.data == 'pay_access', state=MenuState.main_menu)
async def pay_access_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="1 месяц ($155)", callback_data='pay_1_month'))
    keyboard.add(InlineKeyboardButton(text="3 месяца ($400)", callback_data='pay_3_months'))
    keyboard.add(InlineKeyboardButton(text="6 месяцев ($700)", callback_data='pay_6_months'))
    keyboard.add(InlineKeyboardButton(text="1 год ($1200)", callback_data='pay_1_year'))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data='back_to_menu'))

    try:
        await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id,
                                    text="Выберите срок подписки:",
                                    reply_markup=keyboard)
    except MessageNotModified:
        pass

async def handle_payment_period(callback_query: types.CallbackQuery, period_text: str, payment_url: str):
    await callback_query.answer()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="💵Оплатить", url=payment_url))
    keyboard.add(InlineKeyboardButton(text="❓Как пополнить CryptoBot?", url='https://teletype.in/@ipa_dark/cryptobot'))
    keyboard.add(InlineKeyboardButton(text="✅Я оплатил", callback_data=f'payment_check_{period_text}'))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data='pay_access'))

    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text=f"Вы выбрали подписку на {period_text}. Следуйте инструкциям ниже:",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'pay_1_month', state=MenuState.main_menu)
async def pay_1_month_callback(callback_query: types.CallbackQuery):
    await handle_payment_period(callback_query, "1 месяц", 'https://t.me/send?start=IVoCFekRfe7q')

@dp.callback_query_handler(lambda c: c.data == 'pay_3_months', state=MenuState.main_menu)
async def pay_3_months_callback(callback_query: types.CallbackQuery):
    await handle_payment_period(callback_query, "3 месяца", 'https://t.me/send?start=IVJvRYxMw339')

@dp.callback_query_handler(lambda c: c.data == 'pay_6_months', state=MenuState.main_menu)
async def pay_6_months_callback(callback_query: types.CallbackQuery):
    await handle_payment_period(callback_query, "6 месяцев", 'https://t.me/send?start=IV7uyt4UaFZV')

@dp.callback_query_handler(lambda c: c.data == 'pay_1_year', state=MenuState.main_menu)
async def pay_1_year_callback(callback_query: types.CallbackQuery):
    await handle_payment_period(callback_query, "1 год", 'https://t.me/send?start=IV9MVPdk0K2n')

# Проверка статуса платежа
@dp.callback_query_handler(lambda c: c.data.startswith('payment_check_'), state=MenuState.main_menu)
async def payment_check_callback(callback_query: types.CallbackQuery):
    period_text = callback_query.data.split('_')[-1]
    invoice_id = 'example_invoice_id'  # Здесь должна быть реальная логика получения ID платежа
    payment_status = await check_payment_status(invoice_id)
    if payment_status:
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text="👤МЕНЕДЖЕР", url='https://t.me/your_manager_bot')
        )
        await bot.send_message(callback_query.from_user.id, "Платеж пройден, чтобы получить доступ к приватному боту напишите менеджеру.", reply_markup=keyboard)
    else:
        await bot.answer_callback_query(callback_query.id, "Платеж не найден. Оплатите выбранный вами период.", show_alert=True)

# Функция для проверки статуса платежа
async def check_payment_status(invoice_id):
    url = f'https://api.telegram.org/bot{CRYPTOBOT_API_TOKEN}/getInvoiceStatus?invoice_id={invoice_id}'
    response = requests.get(url)
    data = response.json()
    if data['ok'] and data['result']['state'] == 'paid':
        return True
    else:
        return False

# Обработчик нажатий на кнопку "Больше о приватном канале"
@dp.callback_query_handler(lambda c: c.data == 'more_about_private_channel', state=MenuState.main_menu)
async def more_about_private_channel_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    more_info_text = (
        "Что такое Diana brilliant content 🍓?\n\n"
        "Это закрытый доступ ко мне и моему миру откровений, где ты почувствуешь всю глубину страсти и желания.\n\n"
        "То, что ты найдёшь здесь, — особенные моменты, созданные для наслаждения, и интимные секреты, которыми я делюсь только с тобой.\n\n"
        "▫️Каждую неделю я провожу эфиры и делаю уникальные кружочки, которые никому не покажу, кроме своих избранных 😈\n"
        "▫️Хочешь заглянуть в мои фантазии и разделить со мной чувственные моменты? — Присоединяйся, и я покажу, что такое настоящая откровенность.\n\n"
        "▫️В канале получишь доступ к моим аудио, личным историям и видео, которые заставят твоё сердце биться быстрее.\n\n"
        "▫️Также я публикую танцы и стриптиз, чтобы подарить моменты, наполненные искушением и соблазном, которые ты не увидишь больше нигде 🔥\n\n"
        "Для тебя это всё по символической цене, как для моего избранного гостя.\n\n"
        "В каждом из нас есть желания, которые хочется раскрыть. В этом сообществе ты не один: тебя окружают те, кто, как и ты, жаждет страсти, удовольствия и бесконечной откровенности.\n\n"
        "Я готова подарить тебе всё, что держала для избранных.\n\n"
        "Готов присоединиться ко мне? 🫦"
    )
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data='back_to_menu'))
    keyboard.add(InlineKeyboardButton(text="💵Оплатить доступ", callback_data='pay_access'))

    try:
        await bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=more_info_text,
            reply_markup=keyboard
        )
    except MessageNotModified:
        pass

# Обработчик нажатий на кнопку "Назад"
@dp.callback_query_handler(lambda c: c.data == 'back_to_menu', state=MenuState.main_menu)
async def back_to_menu_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await start_command(callback_query.message, state)

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
