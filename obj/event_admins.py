from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class EventAdmins(Base):
    __tablename__ = 'event_admins'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    event_id = Column(Integer(), nullable=False)
    user_id = Column(String(1000), nullable=False)
    user_permission = Column(String(255), nullable=False)

