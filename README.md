# Как запустить проект на dev-server

- Копируем проект к себе по SSH `git@github.com:apaffka/weather-test.git`  

- Устанавливаем зависимости `pip install -r requirements.txt`

- Проводим миграции:  
`cd weather`  
`python3 manage.py makemigrations`  
`python3 manage.py migrate`  

- Создаём суперпользователя `python3 manage.py createsuperuser`

- Заполняем .ENV по шаблону (расположение в папке weather):  

**API_LINK** = 'https://api.weather.yandex.ru/v2/forecast/' (ссылка на момент написания)  
**DJANGO_SECRET_KEY** = ключ Djano  
**DEBUG_PARAM** = True or False  
**YANDEX_WEATHER_TOKEN** = Токен для API Yandex Weather

- Запускаем dev-server `python3 manage.py runserver`  
http://127.0.0.1:8000  

### Возможности
Функционалом предусмотрен ввод города или адреса на русском или английском языке.  
После нажатия кнопки **Получить погоду**, будет скачан файл с прогнозом на 7 дней
или будет выдана ошибка для пользователя.  

При авторизации на сайте в разделе логи будет выводиться информация о запросах и статусах

### Не успел доделать
Не смог реализовать вывод понижения или повышения давления, временно сделал как
информацию о сильном изменении давления (колонка Предупреждения)