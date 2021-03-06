from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QTextEdit, QDateEdit, QDoubleSpinBox, QHBoxLayout, \
    QVBoxLayout, QLabel, QSpacerItem
from manager.common.sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from manager.entities.TransactionsEntity import TransactionsEntity
import requests
import json


class QTransactionsAdd(QWidget):
    Session: sessionmaker = sessionmaker(bind=engine)
    entities: Session = Session()

    label_date: QLabel
    label_currency: QLabel
    label_currency: QLabel
    label_type: QLabel
    label_amount: QLabel
    label_describe: QLabel
    date: QDateEdit
    describe: QTextEdit

    closed: pyqtSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add a transaction")
        self.resize(950, 450)

        # QLabels
        self.label_date = QLabel("Date of transaction :")
        self.label_currency = QLabel("Currency :")
        self.label_type = QLabel("Type of transaction :")
        self.label_amount = QLabel("Amount :")
        self.label_describe = QLabel("Describe :")

        # Date
        self.date = QDateEdit(QDate.currentDate())
        self.date.setDisplayFormat("dd/MM/yyyy")

        # Currencies combobox
        self.currency = QComboBox()
        self.currency.addItem("BTC")
        self.currency.addItem("ETH")
        self.currency.addItem("LTC")
        self.currency.addItem("WXT")
        self.currency.addItem("XRP")
        self.currency.addItem("XLM")
        self.currency.addItem("WAVES")
        self.currency.addItem("WLO")
        self.currency.addItem("DAI")
        self.currency.addItem("NANO")
        self.currency.addItem("EUR")
        self.currency.addItem("USD")

        self.type_transaction = QComboBox()
        self.type_transaction.addItem("Credits")
        self.type_transaction.addItem("Debits")

        self.amount = QDoubleSpinBox()
        self.amount.setValue(0)
        self.amount.setDecimals(8)
        self.amount.setSingleStep(0.00000001)
        self.amount.setSuffix(" " + self.currency.currentText())

        spacer_describe = QSpacerItem(1, 15)
        self.describe = QTextEdit()

        validate_button = QPushButton("Validate")
        cancel_button = QPushButton("Cancel")

        # Vertical layout for date
        vlayout_date = QVBoxLayout()
        vlayout_date.addWidget(self.label_date)
        vlayout_date.addWidget(self.date)

        # Vertical layout for currencies
        vlayout_currency = QVBoxLayout()
        vlayout_currency.addWidget(self.label_currency)
        vlayout_currency.addWidget(self.currency)

        # Vertical layout for type of transaction
        vlayout_type = QVBoxLayout()
        vlayout_type.addWidget(self.label_type)
        vlayout_type.addWidget(self.type_transaction)

        # Vertical layout for amount
        vlayout_amount = QVBoxLayout()
        vlayout_amount.addWidget(self.label_amount)
        vlayout_amount.addWidget(self.amount)

        # Horizontal layout for transaction form
        hlayout_transaction = QHBoxLayout()
        hlayout_transaction.addLayout(vlayout_date)
        hlayout_transaction.addLayout(vlayout_currency)
        hlayout_transaction.addLayout(vlayout_type)
        hlayout_transaction.addLayout(vlayout_amount)

        # Vertical layout for describe
        vlayout_describe = QVBoxLayout()
        vlayout_describe.addSpacerItem(spacer_describe)
        vlayout_describe.addWidget(self.label_describe)
        vlayout_describe.addWidget(self.describe)

        spacer_desc_buttons = QSpacerItem(1, 180)

        # Vertical layout for buttons
        vlayout_buttons = QVBoxLayout()
        vlayout_buttons.addWidget(validate_button)
        vlayout_buttons.addWidget(cancel_button)
        vlayout_buttons.addSpacerItem(spacer_desc_buttons)

        spacer_desc_buttons = QSpacerItem(30, 1)

        # Horizontal layout for describe & buttons
        hlayout_desc_buttons = QHBoxLayout()
        hlayout_desc_buttons.addLayout(vlayout_describe)
        hlayout_desc_buttons.addSpacerItem(spacer_desc_buttons)
        hlayout_desc_buttons.addLayout(vlayout_buttons)
        hlayout_desc_buttons.addSpacerItem(spacer_desc_buttons)

        # Vertical layout for transaction layout & describe & buttons
        vertical_layout = QVBoxLayout(self)
        vertical_layout.addLayout(hlayout_transaction)
        vertical_layout.addLayout(hlayout_desc_buttons)

        # Add signal event in clicked cancel button
        cancel_button.clicked.connect(self.on_clicked_cancel_button)

        # Add signal event in clicked validate button
        validate_button.clicked.connect(self.on_clicked_validate_button)

        # Add signal event in change currency ComboBox
        self.currency.currentTextChanged.connect(self.on_currenttextchanged_currency_combobox)

    def on_clicked_cancel_button(self):
        self.close()

    def on_currenttextchanged_currency_combobox(self):
        self.amount.setSuffix(" " + self.currency.currentText())

    def on_clicked_validate_button(self):
        transaction = TransactionsEntity()
        transaction.date = self.date.date().toPyDate()
        transaction.currency = self.currency.currentText()
        transaction.type = self.type_transaction.currentIndex()
        transaction.amount = self.amount.value()
        transaction.describe = self.describe.toPlainText()

        if not self.currency.currentText() == 'BTC':
            transaction.btc = self.calc_price(self.currency.currentText(), 'BTC')
        else:
            transaction.btc = 0

        transaction.eur = self.calc_price(self.currency.currentText(), 'EUR')
        transaction.usd = self.calc_price(self.currency.currentText(), 'USD')

        self.entities.add(transaction)
        self.entities.commit()
        self.close()

    def calc_price(self, crypto, currency_dest='EUR') -> float:
        price: float = 0
        value: float = 0
        url = 'https://api.coinbase.com/v2/prices/'

        if crypto == "ETH" or crypto == "LTC" or crypto == "XRP" or crypto == "XLM" or crypto == "DAI":
            if self.type_transaction.currentIndex() == 0:
                if currency_dest == 'BTC':
                    price = float(json.loads(requests.get(url + crypto + '-' + 'USD/sell').content)['data']['amount'])
                    value = self.amount.value() * price

                    price = float(json.loads(requests.get(url + 'BTC-USD/sell').content)['data']['amount'])
                    value = value / price
                else:
                    price = float(json.loads(requests.get(url + crypto + '-'+currency_dest+'/sell').content)['data']['amount'])
                    value = self.amount.value() * price
            else:
                if currency_dest == 'BTC':
                    price = float(json.loads(requests.get(url + crypto + '-' + 'USD/buy').content)['data']['amount'])
                    value = self.amount.value() * price

                    price = float(json.loads(requests.get(url + 'BTC-USD/buy').content)['data']['amount'])
                    value = value / price
                else:
                    price = float(json.loads(requests.get(url + crypto + '-'+currency_dest+'/buy').content)['data']['amount'])
                    value = self.amount.value() * price
        elif crypto == 'BTC':
            if self.type_transaction.currentIndex() == 0:
                price = float(json.loads(requests.get(url + crypto + '-' + currency_dest + '/sell').content)['data']['amount'])
                value = self.amount.value() * price
            else:
                price = float(json.loads(requests.get(url + crypto + '-' + currency_dest + '/buy').content)['data']['amount'])
                value = self.amount.value() * price

        return value

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.closed.emit()
