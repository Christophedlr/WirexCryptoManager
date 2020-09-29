from manager.common.sqlalchemy import engine, Base
from manager.entities import TransactionsEntity

if __name__ == "__main__":
    Base.metadata.create_all(engine)
