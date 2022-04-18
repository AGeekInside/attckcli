from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AttckMatrix(Base):
    __tablename__ = "attck_matrix"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    version = Column(String(20))
    attck_id = Column(String(75))



