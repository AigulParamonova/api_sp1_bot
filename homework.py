import logging
import os
import time

import requests
from dotenv import load_dotenv
from telegram import Bot, error

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('main.log')
stream_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


PRAKTIKUM_TOKEN = os.environ.get('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
SLEEP_TIME_BOT = 5 * 60
SLEEP_TIME_EXCEPTIONS = 5
STATUSES = {
    'reviewing': 'Работа взята в ревью!',
    'rejected': 'К сожалению, в работе нашлись ошибки.',
    'approved': 'Ревьюеру всё понравилось, работа зачтена!',
}


bot = Bot(token=TELEGRAM_TOKEN)


class UnexpectedResponseException(Exception):
    pass


def parse_homework_status(homework):
    """Получаем статус проверки домашней работы."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None:
        logging.error(f'Неожиданный ответ от сервера: {homework_name}')
        raise UnexpectedResponseException()
    if homework_status is None:
        logging.error(f'Неожиданный ответ от сервера: {homework_status}')
        raise UnexpectedResponseException()
    if homework_status in STATUSES:
        verdict = STATUSES[homework_status]
        return f'У вас проверили работу "{homework_name}"!\n\n {verdict}'
    else:
        logging.error(f'Неверный статус работы: {homework_status}')
        raise UnexpectedResponseException()


def get_homeworks(current_timestamp):
    """Получаем статус проверки в данный момент времени."""
    payload = {'from_date': current_timestamp}
    if current_timestamp is None:
        current_timestamp = int(time.time())
    else:
        logging.error(f'Неверное значение даты: {current_timestamp}')

    try:
        homework_statuses = requests.get(URL, headers=HEADERS, params=payload)
    except requests.RequestException as e:
        logging.error(f'Не удалось осуществить запрос, ошибка: {e}')
        raise UnexpectedResponseException()

    homework_statuses_json = homework_statuses.json()
    if 'error' in homework_statuses_json:
        raise UnexpectedResponseException()
    if 'code' in homework_statuses_json:
        raise UnexpectedResponseException()
    return homework_statuses_json


def send_message(message):
    """Отправляем сообщение в чат телеграмма."""
    try:
        return bot.send_message(chat_id=CHAT_ID, text=message)
    except error.TelegramError as e:
        logging.error(f'Телеграм не отвечает, перезвоните позже: {e}')


def main():
    """
    Отслеживаем изменение статуса домашней работы
    и уведомляем, в случае изменения.
    """
    logging.debug('Запуск бота')
    current_timestamp = int(time.time())
    while True:
        try:
            my_homework = get_homeworks(current_timestamp)
            if my_homework.get('homeworks'):
                send_message(parse_homework_status(
                    my_homework.get('homeworks')[0])
                )
            logging.info('Сообщение отправлено')
            time.sleep(SLEEP_TIME_BOT)

        except Exception as e:
            logging.error(f'Бот упал с ошибкой: {e}')
            time.sleep(SLEEP_TIME_EXCEPTIONS)


if __name__ == '__main__':
    main()
