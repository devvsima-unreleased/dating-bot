from aiogram.fsm.state import State, StatesGroup


class LikeResponse(StatesGroup):
    response = State()


class ProfileCreate(StatesGroup):
    gender = State()
    find_gender = State()
    photo = State()
    name = State()
    age = State()
    city = State()
    desc = State()


class ProfileEdit(StatesGroup):
    photo = State()
    desc = State()


class Search(StatesGroup):
    search = State()


class Mailing(StatesGroup):
    message = State()


class OfferCreate(StatesGroup):
    photo = State()
    name = State()
    age = State()
    location = State()
    service_types = State()
    description = State()


class OfferEdit(StatesGroup):
    photo = State()
    description = State()
