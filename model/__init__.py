from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from config import config

engine = create_engine('postgresql+psycopg2://' + config.db['db_connect_string'],
                       connect_args={'options': '-csearch_path={}'.format(config.db['db_schema'])},
                       echo=True, future=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()
metadata_obj = MetaData()

alphavantagePrefix = 'https://www.alphavantage.co/query'  # 5/min, 500/day
eodPrefix = 'https://eodhistoricaldata.com/api/'
