import sqlite3
from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class DBSaper(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gamerStat.ui', self)
        self.con = sqlite3.connect('films.db')
        self.addfilm.clicked.connect(self.addFilmWindow)
        self.showAll_b.clicked.connect(self.showAllBook)
        self.genres = []

    def showAllBook(self):
        cur = self.con.cursor()
        result = []
        for i in range(0, 18000, 1000):
            result += cur.execute(
                '''Select title, year, genre, duration from Films WHERE id BETWEEN ? AND ?''', (i, i + 1000)).fetchall()
        self.tableWidget.setRowCount(len(result) + 1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('Title'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Year'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('Genre'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('Duration'))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                if j == 2:
                    temp = cur.execute('Select title from genres WHERE id = ?', (val,)).fetchall()[0][0]
                    self.tableWidget.setItem(i + 1, j,
                                             QTableWidgetItem(' '.join([i.capitalize() for i in temp.split()])))
                    continue
                self.tableWidget.setItem(i + 1, j, QTableWidgetItem(str(val).capitalize()))
        self.tableWidget.resizeColumnsToContents()

    def addFilmWindow(self):
        win = filmsAdder(self)
        win.show()

    def resOfSearch(self, arg, title=False, year=False, duration=False):
        cur = self.con.cursor()
        result = []
        if title:
            result = cur.execute('Select title, year, genre, duration from Films WHERE title like ?',
                                 ('%' + arg + '%',)).fetchall()[:1]
        elif year:
            result = cur.execute('Select title, year, genre, duration from Films WHERE year = ?',
                                 (arg,)).fetchall()[:1]
        elif duration:
            result = cur.execute('Select title, year, genre, duration from Films WHERE duration = ?',
                                 (arg,)).fetchall()[:1]
        self.tableWidget.setRowCount(len(result) + 1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setItem(0, 0, QTableWidgetItem('Title'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Year'))
        self.tableWidget.setItem(0, 2, QTableWidgetItem('Genre'))
        self.tableWidget.setItem(0, 3, QTableWidgetItem('Duration'))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                if j == 2:
                    temp = cur.execute('Select title from genres WHERE id = ?', (val,)).fetchall()[0][0]
                    self.tableWidget.setItem(i + 1, j,
                                             QTableWidgetItem(' '.join([i.capitalize() for i in temp.split()])))
                    continue
                self.tableWidget.setItem(i + 1, j, QTableWidgetItem(str(val).capitalize()))
        self.tableWidget.resizeColumnsToContents()

class filmsAdder(QMainWindow):
    def __init__(self, main):
        super().__init__(main)
        uic.loadUi('addFilmToDB.ui', self)
        self.main = main
        self.pushButton.clicked.connect(self.searchByTitle)
        self.pushButton_2.clicked.connect(self.searchByYear)
        print(1)
        self.pushButton_3.clicked.connect(self.searchByDuration)

    def searchByTitle(self):
        title = self.lineEdit.text()
        self.main.resOfSearch(title, title=True)
        self.close()

    def searchByYear(self):
        year = self.spinBox.value()
        self.main.resOfSearch(year, year=True)
        self.close()

    def searchByDuration(self):
        duration = self.spinBox_2.value()
        self.main.resOfSearch(duration, duration=True)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSaper()
    ex.show()
    sys.exit(app.exec())
