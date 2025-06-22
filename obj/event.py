from sqlalchemy import Column, Integer, String, DateTime, Date, Time, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    event_name = Column(String(255), nullable=False, unique=True)
    event_date = Column(Date())
    nomination_end_timestamp = Column(DateTime())
    voting_end_timestamp = Column(DateTime())
    song_nomination_limit = Column(Integer())
    required_domain = Column(String(255))
    lock_voter_domain = Column(Boolean())
    song_delay = Column(Time())



    # def __init__(
    #         self,
    #         event_name: str,
    #         event_date: date,
    #         nomination_end_timestamp: datetime,
    #         voting_end_timestamp: datetime,
    #         song_nomination_limit: int,
    #         required_domain: str,
    #         song_delay: time,
    #         id: Union[int, None] = None,
    #         lock_voter_domain: bool = False,
    #     ):
    #     self.id=id
    #     self.event_name=event_name
    #     self.event_date=event_date
    #     self.nomination_end_timestamp=nomination_end_timestamp
    #     self.voting_end_timestamp=voting_end_timestamp
    #     self.song_nomination_limit=song_nomination_limit
    #     self.lock_voter_domain= lock_voter_domain | self.domain_validation(required_domain)
    #     self.required_domain=required_domain
    #     self.song_delay=song_delay
    

    



