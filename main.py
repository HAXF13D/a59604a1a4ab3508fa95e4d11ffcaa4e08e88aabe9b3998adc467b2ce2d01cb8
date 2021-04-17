from Rest_api import *
from Functions import *
from aiogram import types, Bot, executor, Dispatcher
from aiogram.types import KeyboardButton as KeyBut
from threading import *

from config import tg_token
# Массив команд для бота
from Txt_Const import COMMANDS

# Объявление текстовых констант
from Txt_Const import START_SCREEN, HELP_SCREEN, ABOUT_SCREEN, STATUS_SCREEN, UPLOAD_SCREEN, \
    IN_WORK_SCREEN, UPLOAD_MESSAGE

# Объявление текстовых сообщений-констант
from Txt_Const import HELP_MSG, START_MSG, STATUS_MSG, SECOND_ERROR_MSG, ERROR_MSG, CHOOSE_MSG, SUCCESS_MSG, \
    STATUS_ERROR_MSG, FILE_ERROR_MSG

# Создание базы данных
make_bd()
bot = Bot(token=tg_token)
dp = Dispatcher(bot)

"""
Обьявление кнопок
"""
button_back = KeyBut('Назад')
button_help = KeyBut('Помощь')
button_status = KeyBut('Статус')
button_about = KeyBut('Описание')
button_upload = KeyBut('Загрузить файл .fpx или .frx')

back_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    button_back)

start_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).row(
    button_upload).add(
    button_about,
    button_help)

in_work_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).row(
    button_upload).row(
    button_status).add(
    button_about,
    button_help)

t1 = Thread(target=misha_func)
t1.start()


# Работа с сообщениями, посылаемыми боту

@dp.message_handler(content_types=['document', 'text'])
async def handle_messages(messages: types.Message):
    message = json.loads(str(messages))

    is_bot = message['from']['is_bot']
    if not is_bot:
        user_id = message['from']['id']
        chat_id = message['chat']['id']
        username = message['from']['first_name']
        user_add(user_id, chat_id, username)
        if message.get('text') is not None:
            # Если сообщение не пустое, переводим в нижний регистр
            msg_text = message['text'].lower()
            # Если сообщение входит в список команд
            if msg_text in COMMANDS:
                cur_screen = user_screen(user_id)
                # Если введена команда /start
                if msg_text == '/start':
                    # Проверка отправлял ли уже пользователь файлы на обработку
                    if req_search(user_id):
                        await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=in_work_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, IN_WORK_SCREEN)
                    else:
                        await bot.send_message(chat_id=chat_id, text=START_MSG, reply_markup=start_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, START_SCREEN)

                # Если введена команда /help
                elif msg_text == '/help':
                    await bot.send_message(chat_id=chat_id, text=HELP_MSG, reply_markup=back_kb,
                                           disable_web_page_preview=True)
                    change_screen(user_id, HELP_SCREEN)

                    # Если введена команда /status
                elif msg_text == '/status':
                    if req_search(user_id):
                        await bot.send_message(chat_id=chat_id, text=STATUS_MSG, reply_markup=back_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, STATUS_SCREEN)
                    else:
                        await bot.send_message(chat_id=chat_id, text=STATUS_ERROR_MSG,
                                               disable_web_page_preview=True)
                # Если текущий экран - начальный
                elif cur_screen == START_SCREEN:
                    # Если поступила команда "описание"
                    if msg_text == 'описание':
                        await bot.send_message(chat_id=chat_id, text=START_MSG, reply_markup=back_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, ABOUT_SCREEN)

                    # Если поступила команда на загрузку файла
                    elif msg_text == 'загрузить файл .fpx или .frx':
                        await bot.send_message(chat_id=chat_id, text=UPLOAD_MESSAGE, reply_markup=back_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, UPLOAD_SCREEN)

                    # Если поступила команда "помощь"
                    elif msg_text == 'помощь':
                        await bot.send_message(chat_id=chat_id, text=HELP_MSG, reply_markup=back_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, HELP_SCREEN)

                # Если текущий экран - экран помощи
                elif cur_screen == HELP_SCREEN:
                    # Если поступила команда "назад"
                    if msg_text == 'назад':
                        # Проверка отправлял ли уже пользователь файлы на обработку
                        if req_search(user_id):
                            await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=in_work_kb,
                                                   disable_web_page_preview=True)
                            change_screen(user_id, IN_WORK_SCREEN)
                        else:
                            await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=start_kb,
                                                   disable_web_page_preview=True)
                            change_screen(user_id, START_SCREEN)

                # Если текущий экран - экран о боте
                elif cur_screen == ABOUT_SCREEN:
                    # Если поступила команда "назад"
                    if msg_text == 'назад':
                        # Проверка отправлял ли уже пользователь файлы на обработку
                        if req_search(user_id):
                            await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=in_work_kb,
                                                   disable_web_page_preview=True)
                            change_screen(user_id, IN_WORK_SCREEN)
                        else:
                            await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=start_kb,
                                                   disable_web_page_preview=True)
                            change_screen(user_id, START_SCREEN)

                # Если текущий экран - экран проверки статуса обработки файла
                elif cur_screen == STATUS_SCREEN:
                    # Если поступила команда "назад"
                    if msg_text == 'назад':
                        # Проверка отправлял ли уже пользователь файлы на обработку
                        if req_search(user_id):
                            await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=in_work_kb,
                                                   disable_web_page_preview=True)
                            change_screen(user_id, IN_WORK_SCREEN)
                        else:
                            await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=start_kb,
                                                   disable_web_page_preview=True)
                            change_screen(user_id, START_SCREEN)

                # Если текущий экран - экран загрузки файла
                elif cur_screen == UPLOAD_SCREEN:
                    # Если поступила команда "назад"
                    if msg_text == 'назад':
                        # Проверка отправлял ли уже пользователь файлы на обработку
                        if req_search(user_id):
                            await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=in_work_kb,
                                                   disable_web_page_preview=True)
                            change_screen(user_id, IN_WORK_SCREEN)
                        else:
                            await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=start_kb,
                                                   disable_web_page_preview=True)
                            change_screen(user_id, START_SCREEN)

                # Если текущий экран - рабочий экран
                elif cur_screen == IN_WORK_SCREEN:
                    if msg_text == 'загрузить файл .fpx или .frx':
                        await bot.send_message(chat_id=chat_id, text=UPLOAD_MESSAGE, reply_markup=back_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, UPLOAD_SCREEN)
                    elif msg_text == 'описание':
                        await bot.send_message(chat_id=chat_id, text=START_MSG, reply_markup=back_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, ABOUT_SCREEN)

                    elif msg_text == 'статус':
                        await bot.send_message(chat_id=chat_id, text=STATUS_MSG, reply_markup=back_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, STATUS_SCREEN)

                    elif msg_text == 'помощь':
                        await bot.send_message(chat_id=chat_id, text=STATUS_MSG, reply_markup=back_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, HELP_SCREEN)

            # Проверка на неправильную команду
            else:
                await bot.send_message(chat_id=chat_id, text=ERROR_MSG,
                                       disable_web_page_preview=True)

        # Работа с отправкой файла боту
        elif (message.get('document') is not None or message.get('text') is not None) and \
                user_screen(user_id) == UPLOAD_SCREEN:
            if message.get('document') is not None:
                # Загрузка документа в память, если расширение файла - корректное
                if extension(message.get('document').get('file_name')):
                    file_ext = get_extension(message.get('document').get('file_name'))
                    file_info = await bot.get_file(message.get('document').get('file_id'))
                    url = f"https://api.telegram.org/file/bot{tg_token}/{file_info.file_path}"
                    # file = requests.get(url)
                    await bot.send_message(chat_id=chat_id, text=SUCCESS_MSG, reply_markup=in_work_kb)
                    change_screen(user_id, IN_WORK_SCREEN)

                    number = -1
                    for cur_file in files:
                        number = max(number, cur_file.number)
                    number += 1
                    files.insert(0, Files(file_number=number,
                                          file_name=f"report_{number}.{file_ext}",
                                          file_url=url,
                                          user_id=user_id))

                    """
                    Если очередь на сервере пуста, то:
                        мы добавляем файл на сервер
                    ИНАЧАЕ:
                         добавляем файл в БД очереди
                    """
                    """
                    Запускаем асинхронный цикл while true
                        В цикле мы опршиванем сервер, до получения статуса success или ошибки
                    Как только статус == success
                        Мы выводим пользователю, что его файл обработан и отправялем ему файл
                        удаляем файлы с сервера
                        добавляем файл из очереди
                        удаляем файл из очереди тут                        
                    """

                # Вывод ошибки при некорректном расширении файла
                else:
                    await bot.send_message(chat_id=chat_id, text=FILE_ERROR_MSG, reply_markup=back_kb,
                                           disable_web_page_preview=True)
            # Проверка на неправильные команды + обработка кнопки назад в окне загрузки файла
            elif message.get('text') is not None:
                msg_text = message['text'].lower()
                if msg_text == 'назад':
                    if req_search(user_id):
                        await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=in_work_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, IN_WORK_SCREEN)
                    else:
                        await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=start_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, START_SCREEN)
                await bot.send_message(chat_id=chat_id, text=ERROR_MSG,
                                       disable_web_page_preview=True)
            else:
                await bot.send_message(chat_id=chat_id, text=SECOND_ERROR_MSG,
                                       disable_web_page_preview=True)

        else:
            await bot.send_message(chat_id=chat_id, text=SECOND_ERROR_MSG)


"""bot.set_update_listener(handle_messages)
bot.polling(none_stop=True)"""

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
