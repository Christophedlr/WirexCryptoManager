from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QShowEvent
from manager.entities.TransactionsEntity import TransactionsEntity
from sqlalchemy.orm import sessionmaker
from manager.common.sqlalchemy import engine


class QTransactionDetails(QWidget):
    date: QLabel
    transaction: QLabel
    amount: QLabel
    btc: QLabel
    eur: QLabel
    usd: QLabel
    describe: QLabel
    entity: TransactionsEntity

    def __init__(self):
        super().__init__()

        self.resize(570, 165)
        self.setWindowTitle("Details of selected transaction")

        label_date = QLabel("Date:")
        label_transaction = QLabel("Transaction:")
        label_amount = QLabel("Amount:")
        label_btc = QLabel("Bitcoin:")
        label_eur = QLabel("Euro:")
        label_usd = QLabel("US $:")
        label_describe = QLabel("Describe:")

        self.date = QLabel()
        self.transaction = QLabel()
        self.amount = QLabel()
        self.btc = QLabel()
        self.eur = QLabel()
        self.usd = QLabel()
        self.describe = QLabel()

        vbox_date = QVBoxLayout()
        vbox_date.addWidget(label_date)
        vbox_date.addWidget(self.date)

        vbox_transaction = QVBoxLayout()
        vbox_transaction.addWidget(label_transaction)
        vbox_transaction.addWidget(self.transaction)

        vbox_amount = QVBoxLayout()
        vbox_amount.addWidget(label_amount)
        vbox_amount.addWidget(self.amount)

        vbox_btc = QVBoxLayout()
        vbox_btc.addWidget(label_btc)
        vbox_btc.addWidget(self.btc)

        vbox_eur = QVBoxLayout()
        vbox_eur.addWidget(label_eur)
        vbox_eur.addWidget(self.eur)

        vbox_usd = QVBoxLayout()
        vbox_usd.addWidget(label_usd)
        vbox_usd.addWidget(self.usd)

        vbox_describe = QVBoxLayout()
        vbox_describe.addWidget(label_describe)
        vbox_describe.addWidget(self.describe)

        close_button = QPushButton("Close")
        hbox_desc_close = QHBoxLayout()
        hbox_desc_close.addLayout(vbox_describe)
        hbox_desc_close.addWidget(close_button)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_date)
        hbox.addLayout(vbox_transaction)
        hbox.addLayout(vbox_amount)
        hbox.addLayout(vbox_btc)
        hbox.addLayout(vbox_eur)
        hbox.addLayout(vbox_usd)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_desc_close)

    def showEvent(self, a0: QShowEvent) -> None:
        super().__init__()
        self.date.setText(self.entity.date.date().strftime("%d/%m/%Y"))

        if self.entity.type == 0:
            self.transaction.setText("Credits")
        else:
            self.transaction.setText("Debits")

        amount = self.entity.amount
        self.amount.setText("{:0.8f}".format(amount))

        if amount < 0:
            self.amount.setStyleSheet("QLabel { color : red }")
        else:
            self.amount.setStyleSheet("QLabel { color : green }")

        self.btc.setText("{:0.8f}".format(self.entity.btc))
        self.eur.setText("{:0.2f}".format(self.entity.eur))
        self.usd.setText("{:0.2f}".format(self.entity.usd))
        self.describe.setText(self.entity.describe)

    def setEntity(self, entity: TransactionsEntity):
        self.entity = entity
