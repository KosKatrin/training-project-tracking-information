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

Form, Window = uic.loadUiType("generate_event.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

def click_on():
    print(form.plainTextEdit.toPlainText())
    print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))  # Форма выбора даты
    # Считываем дату, которая отображается в календаре
    #print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))

def click_on_calendar():
    global start_date, calc_date  # Глобавльно обращается к 2 переменным
    #form.calendarWidget.selectedDate().toString('dd-MM-yyyy')
    form.dateEdit.setDate(form.calendarWidget.selectedDate())  # Связываем календарь с формой выбора даты
    form.dateEdit.dateChanged.connect(on_dateEdit_change)  # Передаем данные из формы выбора даты в календарь

    calc_date = form.calendarWidget.selectedDate()  # Берем значения из календаря
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

form.pushButton.clicked.connect(click_on)
form.calendarWidget.clicked.connect(click_on_calendar)

# 2 переменные, кторые будут рассчитывать сколько дней осталось до наступления события
start_date = form.calendarWidget.selectedDate()  # текущая дата в календаре
calc_date = form.calendarWidget.selectedDate()  # Будут записываться изменения даты
form.label_4.setText('Трекер события от %s' % start_date.toString('dd-MM-yyyy'))

click_on_calendar()
app.exec()