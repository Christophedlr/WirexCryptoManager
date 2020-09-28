from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QHeaderView
from manager.windows.QTransactionsAdd import QTransactionsAdd


# Window for list transactions
class QTransactionsList(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.tr('List of transactions'))
        self.resize(947, 690)

        # Table for list transactions
        table_widget = QTableWidget(0, 3)
        table_widget.setHorizontalHeaderLabels(["Date", "Currency", "Amount"])
        table_widget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        table_widget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

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
        vertical_layout.addWidget(table_widget)
        vertical_layout.addLayout(horizontal_layout)

        add_button.clicked.connect(self.on_clicked_add_button)

    def on_clicked_add_button(self):
        self.add = QTransactionsAdd()
        self.add.setWindowModality(Qt.ApplicationModal)
        self.add.show()
