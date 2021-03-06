import datetime
from manager.common.sqlalchemy import Base, unsigned_int
from sqlalchemy import Column, Text, Float, DateTime, String


class TransactionsEntity(Base):
    __tablename__ = "transactions"

    id = Column(unsigned_int, primary_key=True)
    date = Column(DateTime, index=True, default=datetime.datetime.now)
    currency = Column(String(length=20), index=True)
    type = Column(unsigned_int, index=True, default=0)
    amount = Column(Float)
    describe = Column(Text)
    btc = Column(unsigned_int, nullable=True)
    eur = Column(unsigned_int, nullable=True)
    usd = Column(unsigned_int, nullable=True)
