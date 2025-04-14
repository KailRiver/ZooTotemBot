import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загружаем токен из .env
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Данные для викторины
ANIMALS = {
    "Альпака": {
        "fact": "Альпаки известны своим мягким и теплым шерстью, которая не содержит ланолина, что делает ее гипоаллергенной.",
        "image": "https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/7ee94b22-86c4-4ae6-a583-00d4e61ea90d.jpeg"
    },
    "Лемур кошачий": {
        "fact": "Лемуры кошачьи — уникальные приматы, обитающие только на Мадагаскаре. Могут прыгать на расстояние до 10 метров!",
        "image": "https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/79da8af4-7f66-45fc-b526-2d2395ebc9a8.jpeg"
    },
    "Амурский тигр": {
        "fact": "Амурские тигры — самые крупные из всех тигров и могут весить до 300 кг. Отличные пловцы!",
        "image": "https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/71062cdc-ae27-432a-84ed-d3743afd903b.jpeg"
    },
    "Белогрудый еж": {
        "fact": "Белогрудые ежи — ночные животные, могут сворачиваться в клубок. Их иглы достигают 3 см в длину.",
        "image": "https://storage.moscowzoo.ru/storage/647edc2a70bb5462366280fc/images/animals/01029a4c-4998-4104-bddb-de67d21dea54.jpeg"
    },
}

QUESTIONS = [
    {
        "text": "Как вы предпочитаете проводить выходные?",
        "options": [
            {"text": "Устраивать пикник с друзьями", "animals": {"Альпака": 2, "Лемур кошачий": 1}},
            {"text": "Читать увлекательные книги", "animals": {"Белогрудый еж": 2}},
            {"text": "Смотреть приключенческие фильмы", "animals": {"Амурский тигр": 2}},
            {"text": "Готовить что-то вкусное", "animals": {"Альпака": 1, "Белогрудый еж": 1}}
        ]
    },
    {
        "text": "Если бы вы могли стать супергероем, какую силу вы бы выбрали?",
        "options": [
            {"text": "Быть невероятно ловким и быстрым", "animals": {"Амурский тигр": 2}},
            {"text": "Разговаривать с животными и понимать их", "animals": {"Лемур кошачий": 2}},
            {"text": "Становиться невидимым и исследовать мир", "animals": {"Белогрудый еж": 1}},
            {"text": "Иметь силу делать людей счастливыми", "animals": {"Альпака": 2}}
        ]
    },
    {
        "text": "Какой ваш любимый способ узнать что-то новое?",
        "options": [
            {"text": "Смотреть документальные фильмы о природе", "animals": {"Амурский тигр": 2}},
            {"text": "Читать о приключениях и открытиях", "animals": {"Белогрудый еж": 2}},
            {"text": "Посещать музеи и выставки", "animals": {"Альпака": 1}},
            {"text": "Участвовать в научных экспериментах", "animals": {"Лемур кошачий": 1}}
        ]
    },
    {
        "text": "Если бы у вас была возможность отправиться в любое место на планете, куда бы вы поехали и почему?",
        "options": [
            {"text": "На тропический остров с белым песком и пальмами", "animals": {"Альпака": 2}},
            {"text": "В джунгли, чтобы увидеть экзотических животных", "animals": {"Лемур кошачий": 2}},
            {"text": "В горы для катания на лыжах или сноуборде", "animals": {"Амурский тигр": 1}},
            {"text": "В старинный город с красивой архитектурой", "animals": {"Белогрудый еж": 1}}
        ]
    }
]


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None,
                       parse_mode=None):
    """Универсальная функция отправки сообщений"""
    try:
        if update.message:
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        elif update.callback_query:
            await update.callback_query.message.reply_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        elif update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("Начать викторину", callback_data='start_quiz')],
        [InlineKeyboardButton("О программе опеки", callback_data='about_program')]
    ]
    await send_message(
        update,
        context,
        "🐾 Привет! Я бот Московского зоопарка.\n"
        "Давай узнаем, какое животное твое тотемное!\n\n"
        "После викторины ты узнаешь интересные факты о своем тотемном животном "
        "и как можно поддержать его через программу опеки.",
        InlineKeyboardMarkup(keyboard)
    )


async def about_program(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Информация о программе опеки"""
    try:
        query = update.callback_query
        await query.answer()

        text = (
            "📢 <b>Программа опеки Московского зоопарка:</b>\n\n"
            "Вы можете стать опекуном одного из наших животных!\n\n"
            "Опекая животное, вы помогаете:\n"
            "- Обеспечивать качественное питание\n"
            "- Поддерживать комфортные условия содержания\n"
            "- Развивать научные программы\n\n"
            "Подробнее: <a href='https://moscowzoo.ru/about/guardianship'>сайт программы опеки</a>"
        )

        keyboard = [
            [InlineKeyboardButton("Начать викторину", callback_data='start_quiz')],
            [InlineKeyboardButton("На главную", callback_data='start')]
        ]

        await send_message(
            update,
            context,
            text,
            InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )

    except Exception as e:
        logger.error(f"Ошибка в about_program: {e}")
        await send_message(update, context, "Произошла ошибка. Пожалуйста, попробуйте снова.")


async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Начало викторины"""
    try:
        if update.callback_query:
            await update.callback_query.answer()

        # Полный сброс данных викторины
        context.user_data.clear()
        context.user_data['current_question'] = 0
        context.user_data['animal_points'] = {animal: 0 for animal in ANIMALS}

        # Всегда отправляем первый вопрос как новое сообщение
        await ask_question(update, context, new_message=True)

    except Exception as e:
        logger.error(f"Ошибка в start_quiz: {e}")
        await send_message(update, context, "Произошла ошибка при запуске викторины. Пожалуйста, попробуйте снова.")


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE, new_message=False) -> None:
    """Задаем вопрос пользователю"""
    try:
        question_num = context.user_data.get('current_question', 0)

        if question_num >= len(QUESTIONS):
            await show_result(update, context)
            return

        question = QUESTIONS[question_num]
        keyboard = []

        for i, option in enumerate(question['options']):
            keyboard.append([InlineKeyboardButton(option['text'], callback_data=f'answer_{i}')])

        text = f"Вопрос {question_num + 1}/{len(QUESTIONS)}\n\n{question['text']}"
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Если это первый вопрос или явно запрошено новое сообщение
        if question_num == 0 or new_message:
            await send_message(update, context, text, reply_markup)
        else:
            try:
                # Пытаемся отредактировать предыдущее сообщение
                query = update.callback_query
                await query.edit_message_text(
                    text=text,
                    reply_markup=reply_markup
                )
            except Exception as edit_error:
                logger.error(f"Ошибка редактирования: {edit_error}")
                # Если не удалось отредактировать, отправляем новое сообщение
                await send_message(update, context, text, reply_markup)

    except Exception as e:
        logger.error(f"Ошибка в ask_question: {e}")
        await send_message(update, context, "Произошла ошибка. Пожалуйста, начните викторину снова.")


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка ответа пользователя"""
    try:
        query = update.callback_query
        await query.answer()

        answer_index = int(query.data.split('_')[1])
        question_num = context.user_data.get('current_question', 0)

        if question_num >= len(QUESTIONS):
            await show_result(update, context)
            return

        chosen_option = QUESTIONS[question_num]['options'][answer_index]

        # Добавляем баллы животным
        for animal, points in chosen_option['animals'].items():
            if animal in context.user_data.setdefault('animal_points', {}):
                context.user_data['animal_points'][animal] += points

        # Переходим к следующему вопросу
        context.user_data['current_question'] = question_num + 1
        await ask_question(update, context)

    except Exception as e:
        logger.error(f"Ошибка в handle_answer: {e}")
        await send_message(update, context, "Произошла ошибка при обработке ответа. Пожалуйста, попробуйте снова.")


async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показываем результат викторины"""
    try:
        query = update.callback_query
        await query.answer()

        animal_points = context.user_data.get('animal_points', {})
        if not animal_points:
            await send_message(update, context, "Произошла ошибка. Не удалось определить результат.")
            return

        result_animal = max(animal_points.items(), key=lambda x: x[1])[0]
        animal_info = ANIMALS.get(result_animal, {})

        message = (
            f"🎉 <b>Твое тотемное животное - {result_animal}!</b>\n\n"
            f"🐾 {animal_info.get('fact', '')}\n\n"
            "Хочешь узнать больше о программе опеки?"
        )

        keyboard = [
            [InlineKeyboardButton("Узнать о программе", callback_data='about_program')],
            [InlineKeyboardButton("Пройти еще раз", callback_data='start_quiz')],
            [InlineKeyboardButton("Поделиться",
                                  url=f"https://t.me/share/url?url=Мое тотемное животное - {result_animal}! Узнай свое: https://t.me/{context.bot.username}")]
        ]

        if animal_info.get('image'):
            try:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=animal_info['image'],
                    caption=message,
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode='HTML'
                )
                return
            except Exception as e:
                logger.error(f"Не удалось отправить фото: {e}")

        await query.edit_message_text(
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='HTML'
        )

    except Exception as e:
        logger.error(f"Ошибка в show_result: {e}")
        await send_message(update, context, "Произошла ошибка при показе результата. Пожалуйста, попробуйте снова.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}", exc_info=context.error)
    if update and hasattr(update, 'effective_chat'):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."
        )


def main() -> None:
    """Запуск бота"""
    if not TOKEN:
        logger.error("Не указан TELEGRAM_TOKEN в .env файле!")
        return

    try:
        application = Application.builder().token(TOKEN).build()

        # Регистрируем обработчики
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CallbackQueryHandler(start_quiz, pattern='^start_quiz$'))
        application.add_handler(CallbackQueryHandler(about_program, pattern='^about_program$'))
        application.add_handler(CallbackQueryHandler(handle_answer, pattern='^answer_'))
        application.add_handler(CallbackQueryHandler(start, pattern='^start$'))

        application.add_error_handler(error_handler)

        logger.info("Бот запущен и работает...")
        application.run_polling()

    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == '__main__':
    main()