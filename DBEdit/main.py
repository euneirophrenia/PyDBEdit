__author__ = 'marcodiv'
#First attempt to create a simple DBEditor, based upon SQLite DB and PySide, for Python 3.4.1


from utils import *
from widgets import TableWidget, SQLWidget, AddTableWidget, WelcomeWid
from PySide import QtGui, QtSql

version="1.0"
f=QtGui.QFont()
f.setRawName("Comic Sans MS")


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.utils=""
        self.setFont(f)
        self.tabellina=[]
        self.addwidg=None
        self.setWindowTitle("DBEdit/QT " + version)
        self.men=self.menuBar()
        self.nuovo=QtGui.QAction(QtGui.QIcon('./icons/databaseAdd.ico'), "New DB", self)
        self.nuovo.triggered.connect(self.createdb)
        self.open= QtGui.QAction(QtGui.QIcon('./icons/databaseOpen.ico'), "Open DB", self)
        self.open.triggered.connect(self.opendbdialog)
        self.file= self.men.addMenu("File")
        self.file.addAction(self.nuovo)
        self.file.addAction(self.open)

        self.db=QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.dbname=""
        self.filen=""
        self.nomi=[]
        self.oggetti=[]

        self.lista=QtGui.QListWidget()
        self.lista.setAlternatingRowColors(True)
        self.lista.setAutoFillBackground(True)

        self.lista.setFont(f)

        self.table=TableWidget(self.lista, self)
        self.lista.itemDoubleClicked.connect(self.table.showtable)
        self.wel=WelcomeWid(self)
        self.setCentralWidget(self.wel)
        self.setMinimumWidth(500)
        self.setMinimumHeight(200)

    def showtable(self, nome):
        self.tabellina.append(SQLWidget(tablename=nome, parente=self))

    def addtable(self):
        self.addwidg=AddTableWidget(self)

    def createtable(self):
        try:
            t=self.addwidg.testo.toPlainText()
            self.utils.exec(t)
            self.refresh()
        except Exception as e:
            QtGui.QErrorMessage(self).showMessage(str(e))

    def createdb(self):
        filedialog = QtGui.QFileDialog()
        filedialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        filedialog.setNameFilter("Database (*.db)")
        filedialog.setDirectory(".")
        filedialog.show()

        if filedialog.exec_():
            filename = filedialog.selectedFiles()[0]
            self.db.close()
            self.opendb(filename)
            self.setWindowTitle("DBEdit - {0}".format(filename))

    def popolalista(self, filename):
        self.utils=DBUtils(filename)
        l=self.utils.listtables()
        self.lista.clear()
        self.nomi=[]
        self.oggetti=[]
        for x in l:
            w=str(x[0]).upper()
            v=QtGui.QListWidgetItem(w)
            self.nomi.append(w)
            self.oggetti.append(v)
            self.lista.addItem(v)
        if len(l)==0:
            self.lista.addItem(QtGui.QListWidgetItem("Niente da mostrare"))
        self.setCentralWidget(self.table)

    def refresh(self):
        self.popolalista(self.filen)
        self.repaint()

    def opendb(self, filename):
        self.db.setHostName("localhost")
        self.dbname = getnamefrompath(filename)
        self.db.setDatabaseName(filename)
        self.db.setUserName("root")
        self.db.setPassword("")
        self.db.open()
        self.popolalista(filename)
        self.filen=filename

    def opendbdialog(self):
        filedialog = QtGui.QFileDialog(self)
        filedialog.setDirectory(".")
        filedialog.setFileMode(QtGui.QFileDialog.AnyFile)
        filedialog.show()

        if filedialog.exec_():
            filename = filedialog.selectedFiles()[0]
            self.db.close()
            self.opendb(filename)
            self.setWindowTitle("DBEdit -{0}".format(self.dbname))


def main():
    app = QtGui.QApplication('')
    main_form = MainWindow()
    main_form.show()
    app.exec_()

if __name__ == '__main__':
    main()
