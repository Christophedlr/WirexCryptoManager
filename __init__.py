import sys
from PyQt5.QtWidgets import QApplication
from manager.windows.QTransactionsList import QTransactionsList

app = QApplication(sys.argv)
transactions_list = QTransactionsList()
transactions_list.show()

if __name__ == "__main__":
    app.exec_()
