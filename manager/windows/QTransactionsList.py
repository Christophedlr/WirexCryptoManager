from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QHeaderView, QTableWidgetItem
from manager.windows.QTransactionsAdd import QTransactionsAdd
from manager.windows.QTransactionDetails import QTransactionDetails
from manager.entities.TransactionsEntity import TransactionsEntity
from sqlalchemy.orm import sessionmaker
from manager.common.sqlalchemy import engine


# Window for list transactions
class QTransactionsList(QWidget):
    Session: sessionmaker = sessionmaker(bind=engine)
    entities: Session = Session()

    table_widget: QTableWidget

    def __init__(self):
        super().__init__()

        self.add = QTransactionsAdd()
        self.details = QTransactionDetails()

        self.setWindowTitle(self.tr('List of transactions'))
        self.resize(947, 690)

        # Table for list transactions
        self.table_widget = QTableWidget(0, 4)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Date", "Currency", "Amount"])
        self.table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_widget.setColumnHidden(0, True)

        # Buttons for open new, options and add window
        new_button = QPushButton("New")
        options_button = QPushButton("Options")
        add_button = QPushButton("Add")

        # Horizontal Layout
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addSpacerItem(QSpacerItem(600, 1))
        horizontal_layout.addWidget(new_button)
        horizontal_layout.addWidget(options_button)
        horizontal_layout.addWidget(add_button)

        # Vertical Layout
        vertical_layout = QVBoxLayout(self)
        vertical_layout.addWidget(self.table_widget)
        vertical_layout.addLayout(horizontal_layout)

        add_button.clicked.connect(self.on_clicked_add_button)
        new_button.clicked.connect(self.on_clicked_new_button)
        self.reload_transactions(self.table_widget)

    def on_clicked_add_button(self):
        self.add.setWindowModality(Qt.ApplicationModal)
        self.add.show()

    # Reload transactions from database
    def reload_transactions(self, table_widget: QTableWidget):
        transactions = self.entities.query(TransactionsEntity).all()

        for transaction in transactions:
            self.table_widget.insertRow(self.table_widget.rowCount())
            self.table_widget.setItem(self.table_widget.rowCount()-1, 0, QTableWidgetItem(str(transaction.id)))
            self.table_widget.setItem(self.table_widget.rowCount()-1, 1, QTableWidgetItem(transaction.date.strftime("%d/%m/%Y")))
            self.table_widget.setItem(self.table_widget.rowCount()-1, 2, QTableWidgetItem(transaction.currency))
            self.table_widget.setItem(self.table_widget.rowCount()-1, 3, QTableWidgetItem('{:.8f}'.format(transaction.amount)))

    def on_clicked_new_button(self):
        index = self.table_widget.currentIndex()
        id = int(self.table_widget.item(index.row(), 0).text())

        self.details.setWindowModality(Qt.ApplicationModal)
        self.details.setEntity(self.entities.query(TransactionsEntity).filter(TransactionsEntity.id == id).first())
        self.details.show()
