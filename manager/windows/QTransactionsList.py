from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QHeaderView, \
    QTableWidgetItem, QMenu, QFileDialog
from PyQt5.QtGui import QShowEvent, QContextMenuEvent
from manager.windows.QTransactionsAdd import QTransactionsAdd
from manager.windows.QTransactionDetails import QTransactionDetails
from manager.entities.TransactionsEntity import TransactionsEntity
from sqlalchemy.orm import sessionmaker
from manager.common.sqlalchemy import engine, Base, json_file
import json
import os
from pathlib import Path


# Window for list transactions
class QTransactionsList(QWidget):
    Session: sessionmaker = sessionmaker(bind=engine)
    entities: Session = Session()

    table_widget: QTableWidget
    context_menu: QMenu

    database_name: str

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
        self.add.closed.connect(self.on_closed_transactions_add)
        self.add.show()

    # Reload transactions from database
    def reload_transactions(self, table_widget: QTableWidget):
        table_widget.setRowCount(0)
        transactions = self.entities.query(TransactionsEntity).all()

        for transaction in transactions:
            self.table_widget.insertRow(self.table_widget.rowCount())
            self.table_widget.setItem(self.table_widget.rowCount() - 1, 0, QTableWidgetItem(str(transaction.id)))
            self.table_widget.setItem(self.table_widget.rowCount() - 1, 1,
                                      QTableWidgetItem(transaction.date.strftime("%d/%m/%Y")))
            self.table_widget.setItem(self.table_widget.rowCount() - 1, 2, QTableWidgetItem(transaction.currency))
            self.table_widget.setItem(self.table_widget.rowCount() - 1, 3,
                                      QTableWidgetItem('{:.8f}'.format(transaction.amount)))

    def on_triggered_detail_action(self):
        index = self.table_widget.currentIndex()
        id = int(self.table_widget.item(index.row(), 0).text())

        self.details.setWindowModality(Qt.ApplicationModal)
        self.details.setEntity(self.entities.query(TransactionsEntity).filter(TransactionsEntity.id == id).first())
        self.details.show()

    # Call reload all transactions
    def on_closed_transactions_add(self):
        self.reload_transactions(table_widget=self.table_widget)

    def showEvent(self, a0: QShowEvent) -> None:
        # disable editable cell
        for row in range(0, self.table_widget.rowCount()):
            for col in range(0, 3):
                item = self.table_widget.item(row, col)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def contextMenuEvent(self, a0: QContextMenuEvent) -> None:
        # Create QMenu for details transaction
        self.context_menu = QMenu()
        detail_action = self.context_menu.addAction("Details")
        action = self.context_menu.exec_(self.mapToGlobal(a0.pos()))

        if action == detail_action:
            self.on_triggered_detail_action()

    def on_clicked_new_button(self):
        self.database_name = QFileDialog.getSaveFileName(self, "Create new database", "", filter="SQLite Database (*.sqlite)")
        filename = Path(self.database_name[0])

        print(filename.name)
        print(filename.parent)

        if not filename.suffix:
            filename = filename.with_suffix(".sqlite")

        json_file['database'] = filename.name

        if str(filename.parent) == os.path.dirname(os.path.abspath('__init__.py')):
            json_file['path'] = 'ROOT_DIR'
        else:
            json_file['path'] = str(filename.parent)

        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(json_file, f, ensure_ascii=False, indent=4)

        #Base.metadata.create_all(engine)
