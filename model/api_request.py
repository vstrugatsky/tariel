from model import Base
from sqlalchemy import Column, Integer, String

class ApiRequest(Base):
    __tablename__ = 'api_requests'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    status_code = Column(Integer)