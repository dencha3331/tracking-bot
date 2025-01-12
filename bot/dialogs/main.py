from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Start,
    SwitchTo,
    Button,
    Back,
    Url,
)
from aiogram_dialog.widgets.text import Format, Const
from magic_filter import F

from states import (
    MainStateGroup,
    PaymentStateGroup,
)

from dialogs.getters_clickers import main_getters_clickers as getters_clicks


main_dialog = Dialog(
    Window(
        Format(
            text="{information_message}\n\n---------------------\n\n",
            when=F["information_message"],
        ),
        Format(
            "У Вас действующая подписка до {end_subscribe} ✅",
            when=F["is_subscribe_user"],
        ),
        Format(
            "Ваша подписка закончилась {end_subscribe_user} ❌",
            when=F["end_subscribe_user"],
        ),
        Format(
            "Здесь какой-то рекламный текст можно❗️❗️❗️",
            when=F["not_subscribe_user"],
        ),
        Url(
            Const("↪️🌐 Перейти в канал ↪️🌐"),
            url=Format("{invite_link}"),
            when=F["invite_link"],
        ),
        Start(
            Const("💲🔂 Продлить подписку 🔂💲"),
            id="renew_subscribe",
            state=PaymentStateGroup.choice_subscribe_length,
            when=F["is_subscribe_user"],
        ),
        Start(
            Const("💲 Оформить подписку 💲"),
            id="new_subscribe1",
            state=PaymentStateGroup.choice_subscribe_length,
            when=F["not_subscribe_user"],
        ),
        Start(
            Const("💲 Оформить подписку 💲"),
            id="new_subscribe2",
            state=PaymentStateGroup.choice_subscribe_length,
            when=F["end_subscribe_user"],
        ),
        Url(
            Const("👨‍💻 Администратор 👨‍💻"),
            url=Format("https://t.me/Desca123"),
        ),
        state=MainStateGroup.main_dialog,
        getter=getters_clicks.main_menu_getter,
    ),
)
