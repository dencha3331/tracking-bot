from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Start,
    Url,
    Back,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Format, Const
from magic_filter import F

from configs import settings
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
            "Ваша подписка действует до: {end_subscribe} ✅",
            when=F["is_subscribe_user"],
        ),
        Format(
            "Ваша подписка закончилась {end_subscribe} ❌",
            when=F["end_subscribe_user"],
        ),
        Format(
            "🌟 Добро пожаловать в Пространство Развития!\n\nЗдесь вы получите доступ к закрытому "
            "каналу с уникальными материалами по саморазвитию и духовному росту.\n\n"
            "Выберите действие в меню ниже 👇",
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
            on_click=getters_clicks.cancel_button,
            state=PaymentStateGroup.choice_subscribe_length,
            when=F["is_subscribe_user"],
        ),
        Start(
            Const("💲 Оформить подписку 💲"),
            id="new_subscribe1",
            on_click=getters_clicks.cancel_button,
            state=PaymentStateGroup.choice_subscribe_length,
            when=F["not_subscribe_user"],
        ),
        Start(
            Const("💲 Оформить подписку 💲"),
            id="new_subscribe2",
            on_click=getters_clicks.cancel_button,
            state=PaymentStateGroup.choice_subscribe_length,
            when=F["end_subscribe_user"],
        ),
        SwitchTo(
            Const("📃 Информация о канале 📃"),
            id="switch_to_chanel_information",
            state=MainStateGroup.chanel_information,
        ),
        Url(
            Const("👨‍💻 Администратор 👨‍💻"),
            url=Format(settings.telegram.admin_link),
        ),
        state=MainStateGroup.main_dialog,
        getter=getters_clicks.main_menu_getter,
    ),
    Window(
        Const(
            text="ℹ️ Информация о канале:\n\n🌟 В этом приватном канале вы найдете:\n"
            "- Уникальные знания об устройстве Вселенной\n"
            "- Прогнозы будущих событий\n"
            "- Исцеляющие практики\n"
            "- Методики избавления от страхов\n"
            "- Эксклюзивный контент\n\n"
            "📌 Доступ предоставляется по подписке"
        ),
        Back(Const("⬅️ Назад ")),
        state=MainStateGroup.chanel_information,
    ),
)
