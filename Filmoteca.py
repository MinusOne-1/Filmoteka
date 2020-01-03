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
        self.addfilm.clicked.connect(self.addFilmWindow)
        self.showAll_b.clicked.connect(self.showAllBook)
        self.genres = []

    def showAllBook(self):
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

    def addFilmWindow(self):
        cur = self.con.cursor()
        if self.genres == []:
            self.genres = list(map(lambda u: u[0],
                                   cur.execute('Select title from genres WHERE id BETWEEN 0 AND 1001').fetchall()))
        win = filmsSearcherByGenre(self)
        win.show()

    def showResOfSearch(self, genre):
        cur = self.con.cursor()
        result = cur.execute('''Select title, year, genre, duration from Films 
        WHERE genre=(Select id from genres WHERE title like ?)''', (genre,)).fetchall()
        self.loadDataToTable(result)


class filmsSearcherByGenre(QMainWindow):
    def __init__(self, main):
        super().__init__(main)
        uic.loadUi('addFilmToDB.ui', self)
        self.main = main
        self.comboBox.addItems(sorted(list(self.main.genres)))
        self.pushButton.clicked.connect(self.findRes)

    def findRes(self):
        genre = self.comboBox.itemText(self.comboBox.currentIndex())
        self.main.showResOfSearch(genre)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSaper()
    ex.show()
    sys.exit(app.exec())
