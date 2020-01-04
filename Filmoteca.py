import sqlite3
from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


# оно ОЧЕНЬ Медленно выводит таблицу, т.к. перебирает полным циклом все почти 18000 и заносит их в таблицу.
# оно работает.
class DBSaper(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gamerStat.ui', self)
        self.con = sqlite3.connect('films.db')
        self.addfilm.clicked.connect(self.findFilmWindow)
        self.showAll_b.clicked.connect(self.showAllFilms)
        self.genres = []

    def showAllFilms(self):
        cur = self.con.cursor()
        result = []
        for i in range(0, 18000, 1000):
            result += cur.execute(
                '''Select title, year, genre, duration from Films WHERE id BETWEEN ? AND ?''', (i, i + 1000)).fetchall()
        self.loadDataToTable(result)

    def loadDataToTable(self, data):
        cur = self.con.cursor()
        self.tableWidget.setRowCount(len(data) + 1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('Title'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Year'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('Genre'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('Duration'))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(data):
            for j, val in enumerate(elem):
                if j == 2:
                    temp = cur.execute('Select title from genres WHERE id = ?', (val,)).fetchall()[0][0]
                    self.tableWidget.setItem(i + 1, j,
                                             QTableWidgetItem(' '.join([i.capitalize() for i in temp.split()])))
                    continue
                self.tableWidget.setItem(i + 1, j, QTableWidgetItem(str(val).capitalize()))
        self.tableWidget.resizeColumnsToContents()

    def findFilmWindow(self):
        cur = self.con.cursor()
        if self.genres == []:
            self.genres = list(map(lambda u: u[0],
                                   cur.execute('Select title from genres WHERE id BETWEEN 0 AND 1001').fetchall()))
        win = filmsFinder(self)
        win.show()

    def findFilm(self, title, year, genre, duration,
                 title_sql_b=False, year_sql_b=False, genre_sql_b=False, duration_sql_b=False):
        cur = self.con.cursor()
        sql_ask = 'SELECT title, year, genre, duration FROM Films \nWHERE '

        if title_sql_b:
            sql_ask += 'title ' + title + ' AND \n'
        else:
            sql_ask += 'title LIKE "%' + title + '%"' + ' AND \n'
        if year_sql_b:
            sql_ask += 'year ' + str(year) + ' AND \n'
        else:
            sql_ask += 'year = ' + str(year) + ' AND \n'
        if genre_sql_b:
            sql_ask += 'genre' + str(genre) + ' AND \n'
        else:
            genre1 = cur.execute('Select id from genres WHERE title like ?', (genre,)).fetchall()[0][0]
            sql_ask += 'genre = ' + str(genre1) + ' AND \n'
        if duration_sql_b:
            sql_ask += 'duration ' + str(duration)
        else:
            sql_ask += 'duration = ' + str(duration)
        res = cur.execute(sql_ask).fetchall()
        self.loadDataToTable(res)


class filmsFinder(QMainWindow):
    def __init__(self, main):
        super().__init__(main)
        uic.loadUi('addFilmToDB.ui', self)
        self.main = main
        self.comboBox.addItems(sorted(list(self.main.genres)))
        self.pushButton.clicked.connect(self.add)

    def add(self):
        title = self.lineEdit.text()
        year = self.spinBox.value()
        genre = self.comboBox.itemText(self.comboBox.currentIndex())
        duration = self.spinBox_2.value()
        title_sql = self.textEdit.toPlainText()
        # булевы переменные - нужны для опрееления введён sql-запрос или же параметр указан напрямую
        title_sql_b = False
        year_sql_b = False
        genre_sql_b = False
        duration_sql_b = False
        # Проверка введён ли sql-запрос в каждое из полей
        if title_sql:
            title = title_sql
            title_sql_b = True
        year_sql = self.textEdit_2.toPlainText()
        if year_sql:
            year_sql_b = True
            year = year_sql
        genre_sql = self.textEdit_3.toPlainText()
        if genre_sql:
            genre_sql_b = True
            genre = genre_sql
        duration_sql = self.textEdit_4.toPlainText()
        if duration_sql:
            duration_sql_b = True
            duration = duration_sql
        # вызов метода поиска фильма в БД
        self.main.findFilm(title, year, genre, duration,
                           title_sql_b, year_sql_b, genre_sql_b, duration_sql_b)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSaper()
    ex.show()
    sys.exit(app.exec())
