import sqlite3

from config import db_name

# Объявление текстовых констант на статус отправки файлов
from Txt_Const import NOT_DONE, DONE, STATUS_ERROR_MSG


def generate_status_msg(user_queue):
    if 5 <= user_queue[0] <= 20:
        file_spell = "файлов"
    elif user_queue[0] % 10 == 1:
        file_spell = "файл"
    elif 2 <= user_queue[0] % 10 <= 4:
        file_spell = "файла"
    else:
        file_spell = "файлов"

    if not len(user_queue[1]) == 0:
        status_msg = f"Всего в очереди {user_queue[0]} {file_spell}\n\n"
        nearest_file = user_queue[0] - user_queue[1][0]
        # Закомментить стркоу ниже, если котики не нужны :(
        status_msg += "А пока вы ждете, держите милого котика :3\n\n"
        for status in user_queue[1]:
            nearest_file = min(user_queue[0] - status, nearest_file)
        status_msg += f"Ближайший файл находится на позиции №{nearest_file}"
        return status_msg
    else:
        return STATUS_ERROR_MSG


# Функция проверки расширения файла
def extension(file_name):
    """
    :param file_name: - имя файла
    :return: Расширение файла
    """
    import re
    result = re.split(r'\.', file_name)
    if result[-1] == 'frx' or result[-1] == 'fpx':
        return True
    else:
        return False


def get_file_name(file_name):
    """
    :param file_name: - имя файла
    :return: Расширение файла
    """
    import re
    result = re.split(r'\.', file_name)
    return result[0]


def get_extension(file_name):
    """
    :param file_name: - имя файла
    :return: Расширение файла
    """
    import re
    result = re.split(r'\.', file_name)
    return result[-1]


# Фунуция создания базы данных, если она ещё не создана
def make_bd():
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    user_id INT PRIMARY KEY,
                     chat_id INT,
                     name TEXT,
                     queue INT,
                     screen TEXT,
                     req_status TEXT)''')
    con.commit()
    con.close()


# Функция проверки отправлял ли уже пользователь какие либо файлы
def req_search(user_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f'''SELECT req_status FROM users WHERE user_id = {user_id}''')
    check = cur.fetchone()[0]

    if check == NOT_DONE:
        result = False
    else:
        result = True
    con.commit()
    con.close()
    return result


# Функция смены статуса отправик файлов на обработку
def change_req(user_id, status):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    query = "UPDATE users SET req_status = '{0}' WHERE user_id = '{1}'".format(status, user_id)

    cur.execute(query)
    con.commit()
    con.close()


# Функция внесения данных нового пользователя в базу данных
def user_add(user_id, chat_id, username):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f'''SELECT user_id FROM users WHERE user_id = {user_id}''')
    status = cur.fetchone()
    if status is None:
        cur.execute(f'''INSERT INTO users(user_id, chat_id, name, queue, screen, req_status) VALUES(
                    '{user_id}', 
                    '{chat_id}', 
                    '{username}', 
                    '0', 
                    'start_screen', 
                    'NOT EVER DONE'
                    )''')
    con.commit()
    con.close()


def get_chat_id(user_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f'''SELECT chat_id FROM users WHERE user_id = {user_id}''')
    result = cur.fetchone()[0]
    con.commit()
    con.close()
    return result


# Функция определения текущего положения пользователя в меню бота
def user_screen(user_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f'''SELECT screen FROM users WHERE user_id = {user_id}''')
    screen = cur.fetchone()[0]
    con.commit()
    con.close()
    return screen


# Функция смены положения пользователя при перемещении по меню бота
def change_screen(user_id, cg_screen):
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    query = "UPDATE users SET screen = '{0}' WHERE user_id = '{1}'".format(cg_screen, user_id)
    cur.execute(query)

    con.commit()
    con.close()


def add_file(user_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f'''SELECT queue FROM users WHERE user_id = {user_id}''')
    number = cur.fetchone()[0]
    query = "UPDATE users SET queue = '{0}', req_status = '{1}' WHERE user_id = '{2}'".format(number + 1,
                                                                                              DONE,
                                                                                              user_id)
    cur.execute(query)
    con.commit()
    con.close()


def remove_file(user_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(f'''SELECT queue FROM users WHERE user_id = {user_id}''')
    number = cur.fetchone()[0]
    if number == 1:
        query = "UPDATE users SET queue = '{0}', req_status = '{1}' WHERE user_id = '{2}'".format(number - 1,
                                                                                                  NOT_DONE,
                                                                                                  user_id)
    else:
        query = "UPDATE users SET queue = '{0}', req_status = '{1}' WHERE user_id = '{2}'".format(number - 1,
                                                                                                  DONE,
                                                                                                  user_id)

    cur.execute(query)
    con.commit()
    con.close()
