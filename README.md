# Tracking Bot

## Описание

Tracking Bot - это бот для Telegram, который позволяет добавлять пользователей в канал только после оплаты подписки. 
И контролю чата/группы/канала подписанных пользователей.

## Требования

- Python 3.12+
- Токен Telegram-бота, который вы получили через [@BotFather](https://t.me/BotFather). 
- Привязанная система оплаты ЮКасса к боту, настроенная через @BotFather (Provider token).
- Получите ключ API, следуя инструкциям и правилам Telegram по адресу https://core.telegram.org/api/obtaining_api_id
- Получить ID Вашего чата/группы/канала можно у [IDBot Finder Pro](https://t.me/get_tg_ids_universeBOT).

## Установка и запуск.

---

Клонировать репозиторий: 
``` bash
git clone https://github.com/username/tracking-bot.git`
cd tracking-bot
```

Заполнить поля в .env файле:
```jsunicoderegexp
BOT_CONFIG__TELEGRAM__TOKEN=
BOT_CONFIG__TELEGRAM__PAYMENT_TOKEN=
BOT_CONFIG__TELEGRAM__CHANEL_ID=

BOT_CONFIG__PYROFORK__APP_ID=
BOT_CONFIG__PYROFORK__APP_HASH=
```
Все остальные необходимые переменные окружения для запуска уже есть в .env.example, но вы можете их переопределить.

---

+ ### С Pip и виртуальным окружением:

#### 1. Создать виртуальное окружение:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 2. Установить зависимости:

``` bash
pip install -r requirements.txt
```

Перейдите в каталог:

```bash
cd bot/
```

Установка таблиц базы данных:

```bash
alembic upgrade head
```

#### 3. Запуск приложения: 

```bash
python3 bot_main.py
```



+ ### C makefile:


Запустить контейнеры с приложением и базой данных:

```bash
make all
```

Запустить только приложение:

```bash
make bot
```

Запустить только базу данных:

```bash
make postgres
```

#### Закрытие контейнеров:

```bash
make all-down  # закрытие приложения и базы данных
make bot-down  # закрытие приложения
make postgres-down  # закрытие базы данных
```

## Использование

1. Добавьте бота в чат или группу как администратора. Бот выкинет всех неоплаченных пользователей кроме администраторов.
2. Для оформления подписки перейдите в бот и запустите.

## Оплата

1. Подключите систему оплаты через Telegram, следуя инструкциям на сайте Telegram.
2. Создайте платежный токен и введите его в BOT_CONFIG__TELEGRAM__PAYMENT_TOKEN в .env файл.
3. Настройте варианты подписки, выбрав один из трех вариантов: 1, 3 или 6 месяцев и установите цену 
в копейках BOT_CONFIG__PRICE__MONTH, BOT_CONFIG__PRICE__THREE_MONTH и BOT_CONFIG__PRICE__SIX_MONTH.

## Лицензия

Этот проект распространяется под лицензией MIT.
