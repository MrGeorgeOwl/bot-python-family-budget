from sqlalchemy import Column, Date, Integer, Numeric, String
from db import Base, init_db

class Transaction(Base):
    id = Column(Integer, primary_key=True)
    author = Column(String)
    date = Column(Date, default=datetime.date.today())
    amount = Column(Numeric(precision=2))
    category = Column(String)
    comment = Column(String)

    def __repr__(self) -> str:
        return f"<Transaction({author=}, {date=}, {amount=}, {category=}, {comment=}"
