import telebot
from telebot import types
import pandas as pd
import random
#from sqlalchemy import create_engine
### токен бота
bot = telebot.TeleBot('7467845294:AAGZzeek0ueWM9w5cUT65Jrf9tRo1UXu_ac')
name = '';
surname = '';
exp=''
salary=''
typejob=''
city=''
age = '';

###

# Путь к .xls файлу
xls_file = "vac.xls"

# Чтение .xls файла
try:
    df = pd.read_excel(xls_file, engine="xlrd")  # Замените engine="openpyxl" для .xlsx файлов
    print("Файл успешно прочитан. Пример данных:")
    print(df.head())
except Exception as e:
    print("Ошибка чтения Excel файла:", e)
    exit()
## функция которая сортирует данные (навыки) с использованием пузырька
def f(df):
    b=[[j.split(',') for j in i.split(';')] for i in df['Навыки'].to_list()]

    c=[]
    for i in b:
        for j in i:
            c.append(j)
    z=[]
    for i in c:
        for j in i:
            if len(j)>1:
                if j[0]==' ' or j[0]=='(':
                    z.append(j[1:])
                else:
                    z.append(j)

    mama=[(i+' '+str(z.count(i))) for i in z if z.count(i)>=2]
    papa=list(set(mama))
    a=papa
    for i in range(len(papa)-1):
        for j in range(len(papa)-1-i):
            if int((a[j])[-2:]) > int((a[j+1])[-2:]):
                a[j], a[j+1] = a[j+1], a[j]
    re = ''
    for i in range(2,20):
        re+=(a[-i])[:-2]+' '
    return re


###

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помощник!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == '👋 Поздороваться' or message.text=='/again':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Составить резюме')
        btn2 = types.KeyboardButton('Чему учиться специалисту по ИБ?')
        btn3 = types.KeyboardButton('Оценить свои шансы')
        btn4 = types.KeyboardButton('Квиз на тему ИБ')
       # btn5 = types.KeyboardButton('Интересные факты про IT')
        markup.add(btn1, btn2, btn3,btn4)
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name} ')
        bot.send_message(message.from_user.id, '❓ Задайте интересующий вас вопрос', reply_markup=markup) #ответ бота


    elif message.text == 'Составить резюме' or message.text == '/reg':    
        check(message)
    elif message.text == 'Чему учиться специалисту по ИБ?':
        learn(message)
    elif message.text == 'Оценить свои шансы':
        #bot.send_message(message.from_user.id, 'Подробно про советы по оформлению публикаций прочитать по ' + '[ссылке](https://habr.com/ru/docs/companies/design/)', parse_mode='Markdown')
        chance(message)
    elif message.text == 'Квиз на тему ИБ':
        start_quiz(message)
    elif message.text not in ['Составить резюме','Квиз на тему ИБ','Оценить свои шансы','Чему учиться специалисту по ИБ?','/reg']:
        z=random.randint(0,1)
        if z==1:
            z='Я думаю, да'
        else:
            z ='Я думаю, нет'
        bot.send_message(message.from_user.id, z)

# Резюме
def check(message):
    bot.send_message(message.chat.id, "Давайте начнем заполнение анкеты.")
    bot.send_message(message.chat.id, "Как Вас зовут?")
    bot.register_next_step_handler(message, get_name)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
        if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
            bot.send_message(call.message.chat.id, 'Запомню : ) /again')
        elif call.data == "no":
             bot.send_message(call.message.chat.id, "Давайте попробуем снова. Напишите /reg, чтобы начать заново.") #переспрашиваем
        elif call.data == 'nop':
             bot.send_message(call.message.chat.id, "Тебе стоит заполнить анкету, нажми /reg")
        elif call.data == 'yesp':
            try:
                 bot.send_message(call.message.chat.id, "Средний уровень з/п в твоём городе - "+str(int(sum(df[df['Город']==city]['Зарплата'].to_list())/len(df[df['Город']==city]['Зарплата'].to_list()))))
                 bot.send_message(call.message.chat.id, "Количество вакансий по вашему запросу составляет - "+str(len((df[df['Город']==city])[df['Опыт работы'] <=int(exp)]))+'; от общего кол-ва - '+str(len(df)))
                 bot.send_message(call.message.chat.id, "Средний уровень з/п по данному типу занятости равен - "+str(int(sum(df[df['Опыт работы']<=int(exp)]['Зарплата'].to_list())/len(df[df['Опыт работы']<=int(exp)]['Зарплата'].to_list()))))
                 bot.send_message(call.message.chat.id, "Максимальная з/п по данному типу занятости равна - "+str(int(max(df[df['Опыт работы']<=int(exp)]['Зарплата'].to_list()))))
                 bot.send_message(call.message.chat.id, "Вот топ 5 вакансий по вашему запросу"+str((((df[df['Город']==city])[df['Опыт работы'] <=int(exp)])).sort_values(by=['Зарплата'], ascending=False).drop(['Количество отзывов о компании на hh.ru','Keywords','Рейтинг компаний на hh.ru ','ID','Город'],axis=1).head()))
                 #Навыки 
                 bot.send_message(call.message.chat.id, "Вот какие требования предъявляет самая популярная компания в вашем городе: "+str((((((df[df['Город']==city])[df['Опыт работы'] <=int(exp)])).sort_values(by=['Зарплата'], ascending=False)['Навыки']).to_list())[0]))
                 bot.send_message(call.message.chat.id, 'А вот самые ключевые навыки по вакании: '+f(df))
            except Exception as e:  bot.send_message(call.message.chat.id, "Введите более корректные данные")


@bot.message_handler(content_types=['text'])
def start(message):
        if message.text == '/reg':
            bot.send_message(message.from_user.id, "Как Вас зовут?");
            bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
        else:
            bot.send_message(message.from_user.id, 'Напиши /reg');
def get_name(message): #получаем фамилию
        global name;
        name = message.text;
        bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
        bot.register_next_step_handler(message, get_surname);
def get_surname(message):
        global surname;
        surname = message.text;
        bot.send_message(message.from_user.id,'Какой у вас опыт работы в сфере информационной безопасности?');
        bot.register_next_step_handler(message, get_exp);
def get_exp(message):
        global exp;
        exp = message.text;
        bot.send_message(message.from_user.id,'На какую зарплату вы рассчитываете?');
        bot.register_next_step_handler(message, get_salary);
def get_salary(message):
        global salary;
        salary = message.text;
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        bn1 = types.KeyboardButton('полный рабочий день')
        bn2 = types.KeyboardButton('гибридный формат')
        bn3 = types.KeyboardButton('удаленно')
        markup.add(bn1, bn2, bn3)
        bot.send_message(message.from_user.id,'Какой тип занятости вы рассматриваете?', reply_markup=markup);
        bot.register_next_step_handler(message, get_typejob);
def get_typejob(message):
        global typejob;
        typejob= message.text;
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        bn1 = types.KeyboardButton('Москва')
        bn2 = types.KeyboardButton('Санкт-Петербург')
        bn3 = types.KeyboardButton('Екатеринбург')
        markup.add(bn1, bn2, bn3)
        bot.send_message(message.from_user.id,'В каком вы городе?', reply_markup=markup);
        bot.register_next_step_handler(message, get_pop);

def get_pop(message):
        global city;
        city = message.text;
        bot.send_message(message.from_user.id,'Сколько Вам лет?');
        bot.register_next_step_handler(message, get_age);


def get_age(message):
        global age;
        age = message.text;
        while age == 0: #проверяем что возраст изменился
            try:
                 age = int(message.text) #проверяем, что возраст введен корректно
            except Exception:
                 bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_yes, key_no)
        #question = 'Тебе '+(age)+' лет, тебя зовут '+name+' '+surname+' '+'Твой опыт в IT = '+exp+' Желаемая з/п - '+salary+'Ты рассматриваешь вакансии с рейтингом от '+pop+'?';
        question = generate_resume(name, surname, age, exp, salary, typejob)
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
def generate_resume(name, surname, age, exp, salary, employment_type):
    
    return f"""
📋 **Резюме специалиста в сфере информационной безопасности**

👤 **ФИО:** {name} {surname}  
🎂 **Возраст:** {age} лет  
💼 **Опыт работы:** {exp}  
💰 **Желаемая зарплата:** {salary}  
📍 **Тип занятости:** {employment_type}  

🔑 **Ключевые навыки:**  
- Анализ и защита данных  
- Работа с системами информационной безопасности  
- Реагирование на инциденты  
- Проведение IT-аудитов  

📜 **Сертификаты:**  
- [Если есть, перечислите]  

✍ **Прочее:** Готов к [командировкам/удалённой работе].


"""
# Чему учиться
def learn(message):
    if message.text == 'Чему учиться специалисту по ИБ?':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Основы информационной безопасности')
        btn2 = types.KeyboardButton('Законодательство и нормативы')
        btn3 = types.KeyboardButton('Технические навыки')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id,'Выберете, чему вы хотите учиться', reply_markup=markup);
        bot.register_next_step_handler(message, get_inf);
def get_inf(message): 
    if message.text=='Основы информационной безопасности':
        bot.send_message(message.from_user.id, '' + '[ссылке](https://habr.com/ru/articles/731702/)', parse_mode='Markdown')
        bot.send_message(message.from_user.id, 'Если хотите вернуться в главное меню нажмите /again')
    elif message.text=='Законодательство и нормативы':
        bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/articles/741686/)', parse_mode='Markdown')
        bot.send_message(message.from_user.id, 'Если хотите вернуться в главное меню нажмите /again')
    elif message.text=='Технические навыки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        btn1 = types.KeyboardButton('Сетевые технологии')
        btn2 = types.KeyboardButton('Операционные системы')
        btn3 = types.KeyboardButton('Криптография')
        btn4 = types.KeyboardButton('Программирование и скрипты')
        btn5 = types.KeyboardButton('Защита приложений')
        markup.add(btn1, btn2, btn3,btn4,btn5)
        bot.send_message(message.from_user.id,'Выберете технические навыки', reply_markup=markup);
        bot.register_next_step_handler(message, tech);
def tech(message):
        if message.text=='Сетевые технологии':
            bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/hubs/network_technologies/articles/)', parse_mode='Markdown')
            bot.send_message(message.from_user.id, 'Если хотите вернуться в главное меню нажмите /again')
        if message.text=='Операционные системы':
            bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/companies/otus/articles/728394/)', parse_mode='Markdown')
            bot.send_message(message.from_user.id, 'Если хотите вернуться в главное меню нажмите /again')
        if message.text=='Криптография':
            bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/hubs/crypto/articles/)', parse_mode='Markdown')
            bot.send_message(message.from_user.id, 'Если хотите вернуться в главное меню нажмите /again')
        if message.text=='Программирование и скрипты':
            bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/companies/ruvds/articles/325522/)', parse_mode='Markdown')
            bot.send_message(message.from_user.id, 'Если хотите вернуться в главное меню нажмите /again')
        if message.text=='Защита приложений':
            bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/companies/otus/articles/847490/)', parse_mode='Markdown')
            bot.send_message(message.from_user.id, 'Если хотите вернуться в главное меню нажмите /again')
# 'Оценить свои шансы'
def chance(message):
    a = 'Твой опыт в IT - '+exp+', ты хочешь работать - '+typejob+', а твой город - '+city+'?'
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yesp')
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='nop')
    keyboard.add(key_yes, key_no)
    bot.send_message(message.from_user.id, text=a, reply_markup=keyboard)
# квиз
def start_quiz(message):
    questions = [
        {"question": "Что такое информационная безопасность?", "answers": ["Защита данных", "Интернет-угрозы", "Безопасность компьютера", "Все ответы верны"], "correct": 3},
        {"question": "Что такое фишинг?", "answers": ["Техника защиты данных", "Мошенничество через электронную почту", "Уязвимость программного обеспечения", "Способ взлома паролей"], "correct": 1},
        {"question": "Какой из этих протоколов используется для безопасной передачи данных в интернете?", "answers": ["HTTP", "FTP", "HTTPS", "SMTP"], "correct": 2},
        {"question": "Какой тип угрозы описывает вирус, который может саморазмножаться?", "answers": ["Червь", "Троян", "Вирус", "Шпионская программа"], "correct": 0},
        {"question": "Какие данные необходимо шифровать при работе с банковскими транзакциями?", "answers": ["Номер карты", "Дата рождения", "Пароль", "Все ответы верны"], "correct": 3}
    ]
    
    # Сохраняем текущий вопрос и номер пользователя
    user_id = message.from_user.id
    current_question = 0
    score = 0
    
    ask_question(user_id, current_question, questions, score)

def ask_question(user_id, current_question, questions, score):
    question = questions[current_question]
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i, answer in enumerate(question["answers"]):
        markup.add(types.KeyboardButton(answer))
    
    # Отправляем вопрос с вариантами ответов
    bot.send_message(user_id, question["question"], reply_markup=markup)
    bot.register_next_step_handler_by_chat_id(user_id, handle_answer, current_question, questions, score)

def handle_answer(message, current_question, questions, score):
    user_answer = message.text
    correct_answer = questions[current_question]["answers"][questions[current_question]["correct"]]
    
    # Проверяем правильность ответа
    if user_answer == correct_answer:
        score += 1
    
    current_question += 1
    
    # Если вопросов больше нет, показываем результат
    if current_question < len(questions):
        ask_question(message.from_user.id, current_question, questions, score)
    else:
        bot.send_message(message.from_user.id, f"Квиз завершён! Ваш результат: {score}/{len(questions)}")
        bot.send_message(message.from_user.id, "Если хотите пройти квиз снова, нажмите /again", reply_markup=types.ReplyKeyboardRemove())

##

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть
