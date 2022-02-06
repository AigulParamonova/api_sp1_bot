## Telegram-бот 

Бот - ассистент, который обращается к API сервиса Практикум.Домашка и узнаёт статус моей домашней работы: взята ли домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

## Технологии:
- Python 3
- Django REST Framework
- Git

## Документация:
https://code.s3.yandex.net/backend-developer/learning-materials/delugov/Практикум.Домашка%20Шпаргалка.pdf

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
`https://github.com/AigulParamonova/api_sp1_bot.git`
`cd api_sp1_bot`

Установите и активируйте виртуальное окружение (Windows):
`python -m venv venv`
`source venv/Scripts/activate`

Установить зависимости:
`pip install -r requirements.txt`

Для работы с базой данных создать файл .env c переменными окружения:
`touch .env`
`PRAKTIKUM_TOKEN='AQAAAAA0-iDeAAYckaOIA-ypQkGctU1CsbcVD9U'`
`TELEGRAM_TOKEN='1838214477:AAFuRvn3FoYG8OJYUSfosVXhUVFRaBdwz7A'`
`TELEGRAM_CHAT_ID=993179656``https://github.com/AigulParamonova/api_sp1_bot.git`
