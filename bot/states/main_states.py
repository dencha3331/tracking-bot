from aiogram.fsm.state import State, StatesGroup


class MainStateGroup(StatesGroup):
    main_dialog = State()
    chanel_information = State()
