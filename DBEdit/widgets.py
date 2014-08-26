__author__ = 'marcodiv'

from PySide import QtGui, QtCore, QtSql
from utils import *

Comicf=QtGui.QFont()
Comicf.setRawName("Comic Sans MS")


class TableWidget(QtGui.QWidget):
    def __init__(self, qlist, parente):
        super(TableWidget, self).__init__()
        self.hbox=QtGui.QHBoxLayout()
        self.parente=parente
        self.lista=qlist
        self.hbox.addWidget(self.lista)
        self.vbox=QtGui.QVBoxLayout()
        self.mostra=QtGui.QPushButton("Show")
        self.mostra.clicked.connect(self.showtable)
        self.vbox.addWidget(self.mostra)
        self.add=QtGui.QPushButton("Add")
        self.add.clicked.connect(self.parente.addtable)
        self.vbox.addWidget(self.add)
        self.exit=QtGui.QPushButton("Exit")
        self.exit.clicked.connect(killshit)
        self.delete=QtGui.QPushButton("Delete")
        self.delete.clicked.connect(self.deletetable)
        self.vbox.addWidget(self.delete)
        self.vbox.addWidget(self.exit)
        self.hbox.addItem(self.vbox)
        self.setLayout(self.hbox)

    def deletetable(self):
        s=self.lista.selectedItems()
        for i in s:
            x=indexofobj(self.parente.oggetti, i)
            if x>=0:
                name=self.parente.nomi[x]
                confirm = QtGui.QMessageBox()
                confirm.setWindowTitle("Cancellazione entry")
                confirm.setText("Attenzione")
                confirm.setInformativeText("Sei sicuro di voler eliminare\n"
                                           "''{0}''\ndal database?\nTutti i dati andranno persi".format(name))
                confirm.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
                res = confirm.exec_()
                if res == QtGui.QMessageBox.Ok:
                    self.parente.utils.droptable(self.parente.nomi[x])
                    self.parente.refresh()

    def showtable(self):
        s=self.lista.selectedItems()
        for x in s:
            i=indexofobj(self.parente.oggetti, x)
            if i>=0:
                name=self.parente.nomi[i]
                self.parente.showtable(name)

    def addwidget(self, wid):
        self.vbox.addWidget(wid)

    def additem(self, it):
        self.vbox.addItem(it)

    def setlist(self, lista):
        self.lista=lista


class SQLWidget(QtGui.QWidget):
    def __init__(self, parente, tablename=None, query=None):
        super(SQLWidget, self).__init__()
        self.decide=False

        self.useful=None

        self.coreview=QtGui.QTableView(self)
        self.coreview.setAlternatingRowColors(True)
        self.coreview.setEditTriggers(QtGui.QTableView.AllEditTriggers)
        self.coreview.resizeRowsToContents()
        self.coreview.resizeColumnsToContents()
        self.coreview.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.setFont(Comicf)
        self.setMinimumHeight(500)
        self.parente=parente

        if query is None and tablename is not None :
            self.setWindowTitle(str(tablename))

            self.attributes=self.parente.utils.getheaderfromtable(tablename)
            self.tabname=tablename

            self.model=QtSql.QSqlQueryModel()
            self.model.setQuery("select * from " + str(tablename))

            self.hbox=QtGui.QHBoxLayout()
            self.coreview.setModel(self.model)
            self.coreview.setSortingEnabled(True)
            self.desc=False
            self.h=self.coreview.horizontalHeader()
            self.connect(self.h, QtCore.SIGNAL("sectionClicked(int)"), self.sortTable)
            self.hbox.addWidget(self.coreview)

            group = QtGui.QGroupBox("Filter")
            grouplayout = QtGui.QGridLayout()

            self.filterDict = {}
            self.linee=[]
            index=0
            for item in self.attributes:
                line = QtGui.QLineEdit()
                self.linee.append(line)
                grouplayout.addWidget(QtGui.QLabel(str(item)), index, 0)
                grouplayout.addWidget(line, index, 1, 1, 2)
                index+=1
                line.textChanged.connect(self.filter)
                self.filterDict[str(item)] = line

            self.reset=QtGui.QPushButton("Reset")
            self.reset.clicked.connect(self.resetta)
            group.setMinimumWidth(200)
            group.setLayout(grouplayout)

            self.vbox=QtGui.QVBoxLayout()
            self.vbox.setSpacing(10)
            self.hbox.setSpacing(10)
            groupadd = QtGui.QGroupBox("Add row")
            grouplayoutadd = QtGui.QGridLayout()

            self.addDict = {}
            index=0
            self.lineeadd=[]
            for item in self.attributes:
                lines= QtGui.QLineEdit()
                self.lineeadd.append(lines)
                grouplayoutadd.addWidget(QtGui.QLabel(str(item)), index, 0)
                grouplayoutadd.addWidget(lines, index, 1, 1, 2)
                index+=1
                self.addDict[str(item)] = lines

            self.addbtn=QtGui.QPushButton("Add Row")
            self.addbtn.clicked.connect(self.addrow)
            groupadd.setMinimumWidth(200)
            groupadd.setLayout(grouplayoutadd)

            self.vbox.addWidget(group)
            self.vbox.addWidget(self.reset)
            self.vbox.addSpacing(30)
            self.vbox.addWidget(groupadd)
            self.vbox.addWidget(self.addbtn)
            self.err=None
            self.hbox.addItem(self.vbox)

            self.vbox2=QtGui.QVBoxLayout()
            self.vbox2.addItem(self.hbox)

            self.hbox2=QtGui.QHBoxLayout()
            self.sql=QtGui.QLineEdit()
            self.hbox2.addWidget(self.sql)
            self.hbox2.setSpacing(10)
            self.runsql=QtGui.QPushButton("Exec sql")
            self.runsql.clicked.connect(self.run)
            self.hbox2.addWidget(self.runsql)

            self.vbox2.addItem(self.hbox2)

            self.setLayout(self.vbox2)

        if query is not None and tablename is None:
            self.decide=query
            tab=self.parente.utils.getnamefromquery(query)
            self.setWindowTitle(str(tab))
            self.attributes=self.parente.utils.getheaderfromquery(query)
            self.tabname=tab
            self.model=QtSql.QSqlQueryModel()
            self.model.setQuery(query)

            self.hbox=QtGui.QHBoxLayout()
            self.coreview.setModel(self.model)
            self.coreview.setSortingEnabled(True)
            self.desc=False
            self.h=self.coreview.horizontalHeader()
            self.connect(self.h, QtCore.SIGNAL("sectionClicked(int)"), self.sortTable)
            self.hbox.addWidget(self.coreview)

            group = QtGui.QGroupBox("Filter")
            grouplayout = QtGui.QGridLayout()

            self.filterDict = {}
            self.linee=[]
            index=0
            for item in self.attributes:
                line = QtGui.QLineEdit()
                self.linee.append(line)
                grouplayout.addWidget(QtGui.QLabel(str(item)), index, 0)
                grouplayout.addWidget(line, index, 1, 1, 2)
                index+=1
                line.textChanged.connect(self.filter)
                self.filterDict[str(item)] = line

            self.reset=QtGui.QPushButton("Reset")
            self.reset.clicked.connect(self.resetta)
            group.setMinimumWidth(200)
            group.setLayout(grouplayout)

            self.vbox=QtGui.QVBoxLayout()
            self.vbox.setSpacing(10)
            self.hbox.setSpacing(10)
            self.vbox.addWidget(group)
            self.vbox.addWidget(self.reset)
            self.vbox.addSpacing(30)

            self.hbox.addItem(self.vbox)

            self.vbox2=QtGui.QVBoxLayout()
            self.vbox2.addItem(self.hbox)

            self.hbox2=QtGui.QHBoxLayout()
            self.sql=QtGui.QLineEdit()
            self.hbox2.addWidget(self.sql)
            self.hbox2.setSpacing(10)
            self.runsql=QtGui.QPushButton("Exec sql")
            self.runsql.clicked.connect(self.run)
            self.hbox2.addWidget(self.runsql)

            self.vbox2.addItem(self.hbox2)

            self.setLayout(self.vbox2)

        if tablename != "Niente da mostrare":
            self.coreview.setMinimumWidth(100 *len(self.attributes) + 15)
            self.show()

    def run(self):
        s=str(self.sql.text())
        try:
            self.parente.utils.exec(s)
            if s.startswith("select "):
                newtabname=self.parente.utils.getnamefromquery(s)
                if newtabname != self.tabname:
                    self.useful=SQLWidget(parente=self.parente, query=s)
                    self.useful.show()
                else:
                    self.model.setQuery(s)
            else:
                self.model.setQuery("select * from "+ self.tabname)
        except Exception as e:
            QtGui.QErrorMessage(self).showMessage(str(e))

    def addrow(self):
        if len(self.attributes)<1:
            return
        param=[]
        stringa="insert into " + str(self.tabname) + " values ( "
        try:
            for i in range(0, len(self.attributes) -1):
                t=self.addDict[str(self.attributes[i])].text()
                stringa+= "?, "
                param.append(t)
            t=self.addDict[str(self.attributes[len(self.attributes)- 1])].text()
            stringa+="?)"
            param.append(t)
            self.parente.utils.exec(stringa, param)
            self.model.setQuery("select * from "+ self.tabname)
        except Exception as e:
            self.err=QtGui.QErrorMessage(self).showMessage(str(e))

    def sortTable(self, section):
        self.desc=not self.desc
        attr=self.attributes[section]
        s="select * from " + str(self.tabname)+ " ORDER BY "+ str(attr)
        if self.desc:
            s+=" DESC"
        else:
            s+=" ASC"
        self.model.setQuery(s)

    def filter(self):
        if len(self.attributes)<1:
            return
        if self.decide:
            self.attributes=self.parente.utils.getheaderfromquery(self.decide)
        stringa="select * from " + str(self.tabname) + " where "
        for i in range(0, len(self.attributes) -1):
            t=self.filterDict[str(self.attributes[i])].text()
            stringa+= str(self.attributes[i]) + " LIKE '" + str(t) + "%' AND "
        t=self.filterDict[str(self.attributes[len(self.attributes)- 1])].text()
        stringa+= str(self.attributes[len(self.attributes)- 1])+ " LIKE '" + str(t) + "%'"
        self.model.setQuery(stringa)

    def resetta(self):
        for x in self.attributes:
            self.filterDict[str(x)].clear()
        self.model.setQuery("select * from "+ str(self.tabname))


class AddTableWidget(QtGui.QDialog):
    def __init__(self, parente, defaultext=None):
        super(AddTableWidget, self).__init__()
        self.parente=parente
        self.setWindowTitle("Add table")
        self.vbox=QtGui.QVBoxLayout()

        self.testo=QtGui.QTextEdit()
        if defaultext is None:
            self.testo.setText("Create table ( \n\n )")
        else:
            self.testo.setText(defaultext)
        self.testo.setFont(Comicf)
        self.ok=QtGui.QPushButton("Confirm")
        self.ok.clicked.connect(self.createtable)
        self.vbox.addWidget(self.testo)
        self.vbox.addWidget(self.ok)

        self.setLayout(self.vbox)
        self.show()

    def createtable(self):
        self.parente.createtable()
        self.close()


class WelcomeWid(QtGui.QWidget):
    def __init__(self, parente):
        super(WelcomeWid, self).__init__()
        self.parente=parente
        self.welcome=QtGui.QLabel("Benvenuto, apri un DB per cominciare")
        self.welcome.setFont(Comicf)
        self.wel=QtGui.QVBoxLayout()
        self.wel.addWidget(self.welcome)
        self.opener=QtGui.QPushButton("Open")
        self.opener.clicked.connect(self.parente.opendbdialog)
        self.newer=QtGui.QPushButton("New")
        self.newer.clicked.connect(self.parente.createdb)

        self.hbox=QtGui.QHBoxLayout()
        self.hbox.addWidget(self.opener)
        self.hbox.addWidget(self.newer)
        self.hbox.setSpacing(10)
        self.wel.addItem(self.hbox)

        self.welcome.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.wel)