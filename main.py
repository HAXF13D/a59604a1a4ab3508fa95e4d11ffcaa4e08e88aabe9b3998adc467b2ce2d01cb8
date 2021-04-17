import random
from threading import *

from aiogram import Bot, executor, Dispatcher

from Functions import *
from Rest_api import *
from Txt_Const import *
from config import tg_token

# Массив команд для бота


# Создание базы данных
make_bd()
bot = Bot(token=tg_token)
dp = Dispatcher(bot)

"""
Обьявление кнопок
"""

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
                    await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=in_work_kb,
                                           disable_web_page_preview=True)
                    change_screen(user_id, IN_WORK_SCREEN)

                # Если введена команда /help
                elif msg_text == '/help':
                    await bot.send_message(chat_id=chat_id, text=HELP_MSG, reply_markup=back_kb,
                                           disable_web_page_preview=True)
                    change_screen(user_id, HELP_SCREEN)

                    # Если введена команда /status
                elif msg_text == '/status':
                    user_queue = check_file_status(user_id)
                    if user_queue is not None:
                        status_msg = generate_status_msg(user_queue)
                        # Код ниже отправляет сообщение без котят :(
                        # await bot.send_message(chat_id=chat_id, text=status_msg, reply_markup=back_kb,
                        #                       disable_web_page_preview=True)
                        random.seed()
                        kitten_number = random.randint(1, 22)
                        path = f'./Kittens/{kitten_number}.jpg'
                        await bot.send_photo(chat_id=chat_id,
                                             photo=open(f'{path}', 'rb'),
                                             caption=status_msg,
                                             reply_markup=back_kb)
                        change_screen(user_id, STATUS_SCREEN)

                    else:
                        await bot.send_message(chat_id=chat_id, text=STATUS_ERROR_MSG,
                                               disable_web_page_preview=True)
                # Если текущий экран - экран помощи
                elif cur_screen in BACK_SCREENS:
                    # Если поступила команда "назад"
                    if msg_text == 'назад':
                        # Проверка отправлял ли уже пользователь файлы на обработку
                        await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=in_work_kb,
                                               disable_web_page_preview=True)
                        change_screen(user_id, IN_WORK_SCREEN)

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
                        user_queue = check_file_status(user_id)
                        if user_queue is not None:
                            status_msg = generate_status_msg(user_queue)
                            # Код ниже отправляет сообщение без котят :(
                            # await bot.send_message(chat_id=chat_id, text=status_msg, reply_markup=back_kb,
                            #                       disable_web_page_preview=True)
                            random.seed()
                            kitten_number = random.randint(1, 22)
                            path = f'./Kittens/{kitten_number}.jpg'
                            await bot.send_photo(chat_id=chat_id,
                                                 photo=open(f'{path}', 'rb'),
                                                 caption=status_msg,
                                                 reply_markup=back_kb)
                            change_screen(user_id, STATUS_SCREEN)
                        else:
                            await bot.send_message(chat_id=chat_id, text=STATUS_ERROR_MSG,
                                                   disable_web_page_preview=True)

                    elif msg_text == 'помощь':
                        await bot.send_message(chat_id=chat_id, text=HELP_MSG, reply_markup=back_kb,
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
                    original_name = message.get('document').get('file_name')
                    url = f"https://api.telegram.org/file/bot{tg_token}/{file_info.file_path}"
                    # file = requests.get(url)
                    add_file(user_id)
                    await bot.send_message(chat_id=chat_id, text=SUCCESS_MSG, reply_markup=in_work_kb)
                    change_screen(user_id, IN_WORK_SCREEN)

                    number = len(files)
                    files.insert(0, Files(file_number=number,
                                          file_name=f"report_{number}.{file_ext}",
                                          original_name=original_name,
                                          file_url=url,
                                          user_id=user_id))
                else:
                    await bot.send_message(chat_id=chat_id, text=FILE_ERROR_MSG, reply_markup=back_kb,
                                           disable_web_page_preview=True)
            # Проверка на неправильные команды + обработка кнопки назад в окне загрузки файла
            elif message.get('text') is not None:
                msg_text = message['text'].lower()
                if msg_text == 'назад':
                    await bot.send_message(chat_id=chat_id, text=CHOOSE_MSG, reply_markup=in_work_kb,
                                           disable_web_page_preview=True)
                    change_screen(user_id, IN_WORK_SCREEN)
                else:
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
