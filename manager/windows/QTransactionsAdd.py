from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QTextEdit, QDateEdit, QDoubleSpinBox, QHBoxLayout, \
    QVBoxLayout, QLabel


class QTransactionsAdd(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add a transaction")
        self.resize(950, 450)

        label_date = QLabel("Date of transaction :")
        label_currency = QLabel("Currency :")
        label_type = QLabel("Type of transaction :")
        label_amount = QLabel("Amount :")
        label_describe = QLabel("Describe :")

        date = QDateEdit(QDate.currentDate())
        date.setDisplayFormat("dd/MM/yyyy")

        currency = QComboBox()
        currency.addItem("BTC")
        currency.addItem("ETH")
        currency.addItem("LTC")
        currency.addItem("WXT")
        currency.addItem("XRP")
        currency.addItem("XLM")
        currency.addItem("WAVES")
        currency.addItem("WLO")
        currency.addItem("DAI")
        currency.addItem("NANO")
        currency.addItem("EUR")
        currency.addItem("USD")

        type_transaction = QComboBox()
        type_transaction.addItem("Credits")
        type_transaction.addItem("Debits")

        amount = QDoubleSpinBox()
        amount.setValue(0)

        describe = QTextEdit()

        validate_button = QPushButton("Validate")
        cancel_button = QPushButton("Cancel")

        vlayout_date = QVBoxLayout()
        vlayout_date.addWidget(label_date)
        vlayout_date.addWidget(date)

        vlayout_currency = QVBoxLayout()
        vlayout_currency.addWidget(label_currency)
        vlayout_currency.addWidget(currency)

        vlayout_type = QVBoxLayout()
        vlayout_type.addWidget(label_type)
        vlayout_type.addWidget(type_transaction)

        vlayout_amount = QVBoxLayout()
        vlayout_amount.addWidget(label_amount)
        vlayout_amount.addWidget(amount)

        hlayout_transaction = QHBoxLayout()
        hlayout_transaction.addLayout(vlayout_date)
        hlayout_transaction.addLayout(vlayout_currency)
        hlayout_transaction.addLayout(vlayout_type)
        hlayout_transaction.addLayout(vlayout_amount)

        vlayout_describe = QVBoxLayout()
        vlayout_describe.addWidget(label_describe)
        vlayout_describe.addWidget(describe)

        vlayout_buttons = QVBoxLayout()
        vlayout_buttons.addWidget(validate_button)
        vlayout_buttons.addWidget(cancel_button)

        hlayout_desc_buttons = QHBoxLayout()
        hlayout_desc_buttons.addLayout(vlayout_describe)
        hlayout_desc_buttons.addLayout(vlayout_buttons)

        vertical_layout = QVBoxLayout(self)
        vertical_layout.addLayout(hlayout_transaction)
        vertical_layout.addLayout(hlayout_desc_buttons)
