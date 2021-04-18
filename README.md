# README


__Реализованная функциональность:__

* Многопоточный режим работы бота
* Бот различает расширение файлов и не позволяет отправлять в облако иные, отличные от ".frx" или ".fpx"
* После принятия файла с расширением ".frx" или ".fpx" бот отправляет его на облако при помощи FastReports REST API
* Бот циклически проверяет статус обработки файла. При получении статуса "Success" бот выходит из цикла и отправляет пользователю отчёт в формате ".pdf"
* Система очереди файлов



__Особенность проекта заключается в:__

* Нестандартном приветствии
* Красивом интерфейсе
* Милых котятах в период ожидания



__Основной стек технологий:__

* Python 3.8, Python 3.9
* Python Aiogram for Telegram Bot API
* sqlite3 
* FastReports REST API
* Методология использования "POST" и "GET" запросов
* GitHub Version Control
* JSON
* XML


__Демо__

Демонстрация работы бота доступна по ссылке в телеграм

* @vert_fastrep_bot

А ещё можно ознакомиться с видеоматериалом, который доступен по ссылкам:

* https://www.youtube.com/watch?v=ebikS8VC1sI&ab_channel=Vovik003
* https://youtube.com/shorts/8m7aalcCmSI?feature=share

__Среда запуска__

Запуск производится на виртуальной машине Google

Ниже представлена ссылка на гайд по запуску бота на виртуальной машине

* https://habr.com/ru/post/488560/

__Разработчики__

* Шальнев Владимир __TeamLead + Developer__
  * __https://vk.com/x_vl_x__
  * __vovik0312@gmail.com__
  
* Выходцев Егор __Developer + Tester__
  * __https://vk.com/n0n4m__
  * __wf-game-acc@bk.ru__

* Духно Михаил __Developer + Tester__
  * __https://vk.com/mishadukhno__
  * __misha.duhno@mail.ru__

* Гробова Софья __Designer__
  * __https://vk.com/grobovaa__
  * __sofya.grobova@yandex.ru__
