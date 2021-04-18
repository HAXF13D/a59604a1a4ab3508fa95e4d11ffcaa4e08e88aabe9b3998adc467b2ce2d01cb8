from aiogram import types
from aiogram.types import KeyboardButton as KeyBut

DONE_MSG = "Ваш файл обработан"

NOT_DONE = "NOT EVER DONE"
DONE = "IN WORK"

button_back = KeyBut('Назад')
button_help = KeyBut('Помощь')
button_status = KeyBut('Статус')
button_about = KeyBut('Описание')
button_upload = KeyBut('Загрузить файл .fpx или .frx')

back_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_back)

in_work_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).row(
    button_upload).row(
    button_status).add(
    button_about,
    button_help)

FILE_NOT_DONE_STATUS = "NOT DONE"
FILE_IN_PROGRESS_STATUS = "IN PROGRESS"
FILE_FINISH_STATUS = "ACCEPT"

COMMANDS = ['/start',
            '/help',
            '/status',
            'назад',
            'помощь',
            'статус',
            'описание',
            'загрузить файл .fpx или .frx']

HELP_SCREEN = "help_screen"
ABOUT_SCREEN = "about_screen"
STATUS_SCREEN = "status_screen"
UPLOAD_SCREEN = "upload_screen"
IN_WORK_SCREEN = "in_work_screen"

UPLOAD_MESSAGE = "Загрузите не более 10 файлов"
"""
HELP_MSG = "Данный бот принимает файлы FRX или FPX и отправляет в ответ сформированный с помощью " \
           "fastreport.cloud/ru/ PDF файл." "\n\nСписок доступных команд:\n" \
           "/start - начать работу\n" \
           "/help - помощь\n" \
           "/status - статус обработки файлов\n" \
           "\nАвторы бота: команда ВЫХОД ЕСТЬ" \
           "\nЕгор Выходцев - vk.com/n0n4m" \
           "\nШальнев Владимир - vk.com/x_vl_x" \
           "\nДухно Михаил - vk.com/mishadukhno" \
           "\nГробова Софья - vk.com/grobovaa"
"""
"""
START_MSG = "Данный бот принимает файлы FRX или FPX и отправляет в ответ сформированный с помощью " \
            "fastreport.cloud/ru/ PDF файл."
"""
HELP_MSG = "Здравствуй, дорогой пользователь!\n" \
           "Меня зовут Верт, и я могу конвертировать файлы формата .fpx и .frx в формат .pdf с помощью " \
           "fastreport.cloud/ru/\n\n" \
           "Я умею:\n" \
           "/start - начать работу\n" \
           "/help - помощь\n" \
           "/status - статус обработки файлов\n" \
           '\nМои создатели: команда "ВЫХОД ЕСТЬ"' \
           "\nЕгор Выходцев - vk.com/n0n4m" \
           "\nШальнев Владимир - vk.com/x_vl_x" \
           "\nДухно Михаил - vk.com/mishadukhno" \
           "\nГробова Софья - vk.com/grobovaa"

START_MSG = "Здравствуй, дорогой пользователь!\n" \
            "Меня зовут Верт, и я могу конвертировать файлы формата .fpx и .frx в формат .pdf с помощью " \
            "fastreport.cloud/ru/"
STATUS_MSG = "Тут будет сообщение статуса"

SECOND_ERROR_MSG = "Я не знаю, что на это ответить, попробуйте еще раз!"
ERROR_MSG = "Неизвестная команда, попробуйте еще раз!"
CHOOSE_MSG = "Выберите действие"
SUCCESS_MSG = "Файл успешно добавлен в очередь"
STATUS_ERROR_MSG = "В настоящий момент у вас нет документов в обработке"
FILE_ERROR_MSG = "Некорректное расширение файла, попробуйте отправить другой файл"
FILE_TO_PDF_ERROR = "Что-то не так с файлом, попробуйте еще раз"

BACK_SCREENS = [
    UPLOAD_SCREEN,
    STATUS_SCREEN,
    ABOUT_SCREEN,
    HELP_SCREEN
]
