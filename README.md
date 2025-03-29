# tgcrawler

Асинхронный телеграм-бот, принимающий excel-файл с источниками в формате title|url|xpath(сайты с первого ряда, без заголовка) и загружающий значения из файла в БД. Записей в файле может быть несколько. Текстовые сообщения бота адаптирован под книжные магазины, но он скушает и посчитает что угодно.
Открывает файл библиотекой pandas, после обработки удаляет из директории проекта.
Выполняет краулинг всех цен с источников, записаных в БД. Использует selenuim и webdriver_manager.chrome для обхода блокировок от ботов.
Из-за синхронной работы selenium применен мультипоток из встроенной библиотеки concurrent.futures.
Умеет отображать все записи из таблицы БД.
Для удобства оставлены логирование и отладочные принты.




Бот - @Test666Crawler_bot. В .env файле вписаны собственные токен и id разработчика. При желании можно поменять на свои или оставить как есть.

1) Установите зависимости из файла requirements.txt (pip install -r requirements.txt)
2) Для подгрузки цен необходимо установить ChromeDriver 
3) Запуск командой uvicorn app.main:app
4) Команда /start откроет главное меню

10 страниц сайтов обходит на моем ПК за ~60-70 секунд.

Стек: FastAPI, uvicorn, aiogram, sqlalchemy, aiosqlite, alembic, pandas, pydantic, pydantic_settings, selenium, webdriver_manager

Ссылка на готовый excel-файл(для примера) с сайтами и xpath для загрузки в чат-бота:
[list_sources.xlsx](https://github.com/user-attachments/files/19522476/list_sources.xlsx)
