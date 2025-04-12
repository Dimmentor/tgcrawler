# tgcrawler

Асинхронный телеграм-бот, принимающий excel-файл с источниками в формате title|url|xpath(сайты с первого ряда, без заголовка) и загружающий значения из файла в БД. Записей в файле может быть несколько. Текстовые сообщения бота адаптирован под книжные магазины, но он скушает и посчитает что угодно.
Открывает файл библиотекой pandas, после обработки удаляет из директории проекта.
Выполняет краулинг всех цен с источников, записаных в БД. Использует selenuim и для обхода блокировок от ботов.
Из-за синхронной работы selenium применен мультипоток из встроенной библиотеки concurrent.futures.
Умеет отображать все записи из таблицы БД.
Для удобства оставлены логирование и отладочные принты.




В .env файле необходимо вписать токен ТГ бота и свой id. 

1) Установите зависимости из файла requirements.txt (pip install -r requirements.txt)
2) Запуск командой uvicorn app.main:app
3) Команда /start откроет главное меню
4) База данных пустая, нужно загрузить excel-файл с источниками, ссылка на готовый ниже:

   
[list_sources2.xlsx](https://github.com/user-attachments/files/19525337/list_sources2.xlsx)
PS: сайты обновляют свои xpath, если бот не смог достучаться на какие-либо сайты, значит xpath необходимо обновить 

10 страниц сайтов обходит на моем ПК за ~60-70 секунд, при условии, если все xpath доступны.

Стек: FastAPI, uvicorn, aiogram, sqlalchemy, aiosqlite, alembic, pandas, , openpyxl, pydantic, pydantic_settings, selenium





