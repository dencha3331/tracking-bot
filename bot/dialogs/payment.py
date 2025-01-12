from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Start,
    SwitchTo,
    Button,
    Back,
    Cancel,
)
from aiogram_dialog.widgets.text import Format, Const
from magic_filter import F

from dialogs.getters_clickers import payment_getters_clickers as getters_clickers
from states import (
    MainStateGroup,
    PaymentStateGroup,
)


payment_dialog = Dialog(
    Window(
        Const("⏳ Выберите на какой период хотите оформить подписку ⏳"),
        Button(
            Const("💲 990 руб на 1 мес"),
            id="go_to_1_month_subscribe",
            on_click=getters_clickers.click_subscribe,
        ),
        Button(
            Const("💲 2490 руб на 3 мес"),
            id="go_to_3_month_subscribe",
            on_click=getters_clickers.click_subscribe,
        ),
        Button(
            Const("💲 4990 руб на 6 мес"),
            id="go_to_6_month_subscribe",
            on_click=getters_clickers.click_subscribe,
        ),
        Cancel(Const("🔙 Назад ⬅️")),
        state=PaymentStateGroup.choice_subscribe_length,
    ),
    Window(
        Const("⬆️ ⬆️ ⬆️ Оплата ⬆️ ⬆️ ⬆️"),
        Back(
            Const("🔙 Назад ⬅️"),
            on_click=getters_clickers.cancel_button,
        ),
        state=PaymentStateGroup.paying,
    ),
)
