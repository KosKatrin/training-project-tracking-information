#from generate_event import*
#import sys

#app = QtWidgets.QApplication(sys.argv)
#MainWindow = QtWidgets.QMainWindow()
#ui = Ui_MainWindow()
#ui.setupUi(MainWindow)
# MainWindow.show()
# sys.exit(app.exec_())

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import pickle

Form, Window = uic.loadUiType("generate_event.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

# Функция, которая сохраняет структуру в файл
def save_to_file():
    global start_date, calc_date, description
    # Тестирование статусной строки. Меняем дату старта, чтобы понять как работает percent
    #start_date = QDate(2021, 12, 1)
    data_to_save = {'start': start_date,
                    'end': calc_date,
                    'description': description}
    file1 = open('config.txt', 'wb')  # Открываем/ если нет создаем файл на запись
    pickle.dump(data_to_save, file1)  # Записываем объект в файл
    file1.close()  # Закрываем файл

# Функция, которая считывает данные из файла
def read_from_file():
    global start_date, calc_date, description, now_date
    try:
        file1 = open('config.txt', 'rb')  # Открываем файл на чтение
        data_to_load = pickle.load(file1)  # Загружаем объект из файла / считываем файл file1
        file1.close()
        # Переопределяем данные
        start_date = data_to_load['start']
        calc_date = data_to_load['end']
        description = data_to_load['description']
        print(start_date.toString('dd-MM-yyyy'), calc_date.toString('dd-MM-yyyy'), description)
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(description)
        
        # Настройка progressBar
        delta_days_left = start_date.daysTo(now_date)   # Прошло дней
        delta_days_right = now_date.daysTo(calc_date)   # Осталось дней
        days_total = start_date.daysTo(calc_date)       # Всего дней
        #print('$$', delta_days_left, delta_days_right, days_total)  #Отладка
        percent = int(delta_days_left * 100 / days_total)
        form.progressBar.setProperty("value", percent)
        #print(percent)  # Отладка
    except:
        print('Не могу прочитать файл конфигурации!')

def click_on():
    global calc_date, description
    calc_date = form.calendarWidget.selectedDate()  # при клике на кнопку будет считываться измененная дата с календаря
    description = form.plainTextEdit.toPlainText()  # при клике на кнопку будет считываться описание события
    # print(form.plainTextEdit.toPlainText())
    # print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))  # Форма выбора даты
    print('Click!')
    save_to_file()  # Вызываем функцию при клике на кнопку "Отследить событие"

def click_on_calendar():
    global start_date, calc_date  # Глобавльно обращается к 2 переменным
    form.dateEdit.setDate(form.calendarWidget.selectedDate())  # Установка даты в dateEdit  на выбранную дату с календаря

    calc_date = form.calendarWidget.selectedDate()  # Дата будет перезаписываться после выбора даты на календаре
    col_days = start_date.daysTo(calc_date)  # Возвращает число дней
    print(col_days)
    form.label_3.setText('До наступления события осталось %s дней' % col_days)

def on_dateEdit_change():
    global start_date, calc_date
    #print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
    form.calendarWidget.setSelectedDate(form.dateEdit.date())

    calc_date = form.dateEdit.date()  # Берем значения из формы dateEdit
    col_days = start_date.daysTo(calc_date)  # Возвращает число дней
    print(col_days)
    form.label_3.setText('До наступления события осталось %s дней' % col_days)

form.pushButton.clicked.connect(click_on)  # Привязываем кнопку к функции click_on. При клике на кнопку вызывается функция
form.calendarWidget.clicked.connect(click_on_calendar)  # Привязываем календарь к функции click_on_calendar. При клике на календарь вызывается функция
form.dateEdit.dateChanged.connect(on_dateEdit_change)  # Привязываем форму выбора даты к функции on_dateEdit_change

# 2 переменные, кторые будут рассчитывать сколько дней осталось до наступления события
start_date = form.calendarWidget.selectedDate()  # стартовая дата в календаре. Определяется при первом запуске приложения
now_date = form.calendarWidget.selectedDate()  # Текущая дата (сегодняшний день в календаре)
calc_date = form.calendarWidget.selectedDate()  # Та дата, относительно которой осталось дней от start_date
description = form.plainTextEdit.toPlainText()

read_from_file()  # Считываем данные из файла
form.label_4.setText('Трекер события от %s' % start_date.toString('dd-MM-yyyy'))  # Текст на экране сколько осталось до события

click_on_calendar()
app.exec()