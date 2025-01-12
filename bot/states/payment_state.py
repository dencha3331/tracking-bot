from aiogram.fsm.state import State, StatesGroup


class PaymentStateGroup(StatesGroup):
    choice_subscribe_length = State()
    one_month_subscribe = State()
    three_month_subscribe = State()
    six_month_subscribe = State()
    paying = State()
