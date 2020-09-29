import datetime
from manager.common.sqlalchemy import Base, unsigned_int
from sqlalchemy import Column, Text, INTEGER, DateTime


class TransactionsEntity(Base):
    __tablename__ = "transactions"

    id = Column(unsigned_int, primary_key=True)
    date = Column(DateTime, index=True, default=datetime.datetime.now)
    currency = Column(unsigned_int, index=True)
    type = Column(unsigned_int, index=True, default='credits')
    amount = Column(INTEGER)
    describe = Column(Text)
