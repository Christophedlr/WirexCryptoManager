import sys
from manager import app
from manager.common.sqlalchemy import engine, Base
from manager.entities import TransactionsEntity


def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    if sys.argv[1] == "init-db":
        init_db()
    else:
        app.exec_()
