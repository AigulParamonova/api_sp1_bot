import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('main.log')
stream_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def parse_homework_status(homework):
    """Получаем комментарий проверки домашней работы."""
    homework_name = homework['homework_name']
    if homework['status'] == 'rejected':
        verdict = 'К сожалению, в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, работа зачтена!'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homeworks(current_timestamp):
    """Получаем статус проверки в данный момент времени."""
    headers = {'Authorization': f'OAuth {TELEGRAM_TOKEN}'}
    payload = {'from_date': current_timestamp}
    homework_statuses = requests.get(URL, headers=headers, params=payload)
    return homework_statuses.json()


def send_message(message):
    """Отправляем сообщение в чат телеграмма."""
    message = 'Проверяем статус ревью домашней работы'
    return bot.send_message(CHAT_ID, message)


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
            time.sleep(5 * 60)

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            logging.error(e, exc_info=True)
            time.sleep(5)


if __name__ == '__main__':
    main()
