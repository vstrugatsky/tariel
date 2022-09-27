from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

dbschema = 'tariel'
engine = create_engine('postgresql+psycopg2://vs@localhost:5432/vs',
                       connect_args={'options': '-csearch_path={}'.format(dbschema)},
                       echo=True, future=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()
metadata_obj = MetaData()

alphavantageApiKey = 'XHQY1H9VZE7QRDDL'     # 5/min, 500/day
alphavantagePrefix = 'https://www.alphavantage.co/query'

eodApiKey = '62e8b0f3e93347.26104179'
eodPrefix = 'https://eodhistoricaldata.com/api/'
