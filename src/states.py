from aiogram.fsm.state import StatesGroup, State

class Admin(StatesGroup):
    movie = State()
    step = State()
    getMovie = State()
    addMovie = State()
    addMovie2 = State()
    delMovie = State()

class User(StatesGroup):
    signIn = State()

class SubChannelState(StatesGroup):
    signin = State()
    add = State()
    list = State()
    remove = State()