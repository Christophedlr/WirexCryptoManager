from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QTextEdit, QDateEdit, QDoubleSpinBox, QHBoxLayout, \
    QVBoxLayout, QLabel, QSpacerItem


class QTransactionsAdd(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add a transaction")
        self.resize(950, 450)

        # QLabels
        label_date = QLabel("Date of transaction :")
        label_currency = QLabel("Currency :")
        label_type = QLabel("Type of transaction :")
        label_amount = QLabel("Amount :")
        label_describe = QLabel("Describe :")

        date = QDateEdit(QDate.currentDate())
        date.setDisplayFormat("dd/MM/yyyy")

        # Currencies combobox
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

        spacer_describe = QSpacerItem(1, 15)
        describe = QTextEdit()

        validate_button = QPushButton("Validate")
        cancel_button = QPushButton("Cancel")

        # Vertical layout for date
        vlayout_date = QVBoxLayout()
        vlayout_date.addWidget(label_date)
        vlayout_date.addWidget(date)

        # Vertical layout for currencies
        vlayout_currency = QVBoxLayout()
        vlayout_currency.addWidget(label_currency)
        vlayout_currency.addWidget(currency)

        # Vertical layout for type of transaction
        vlayout_type = QVBoxLayout()
        vlayout_type.addWidget(label_type)
        vlayout_type.addWidget(type_transaction)

        # Vertical layout for amount
        vlayout_amount = QVBoxLayout()
        vlayout_amount.addWidget(label_amount)
        vlayout_amount.addWidget(amount)

        # Horizontal layout for transaction form
        hlayout_transaction = QHBoxLayout()
        hlayout_transaction.addLayout(vlayout_date)
        hlayout_transaction.addLayout(vlayout_currency)
        hlayout_transaction.addLayout(vlayout_type)
        hlayout_transaction.addLayout(vlayout_amount)

        # Vertical layout for describe
        vlayout_describe = QVBoxLayout()
        vlayout_describe.addSpacerItem(spacer_describe)
        vlayout_describe.addWidget(label_describe)
        vlayout_describe.addWidget(describe)

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

    def on_clicked_cancel_button(self):
        self.close()
