import model as model
from sqlalchemy import Column, String, Text, ForeignKey, PrimaryKeyConstraint


class Exchange(model.Base):
    __tablename__ = 'exchanges'
    operating_mic = Column(String(4), primary_key=True)
    name = Column(Text)
    acronym = Column(String(30))
    iso_country_code = Column(String(2), ForeignKey("countries.iso_code_2"))
    # country = relationship("Country")

    @staticmethod
    def lookup_by_code(exchange: str, session: model.Session):
        return session.query(Exchange.operating_mic).filter(Exchange.operating_mic == exchange).scalar()

    @staticmethod
    def lookup_by_acronym(acronym: str, session: model.Session):
        return session.query(ExchangeAcronym.operating_mic).filter(ExchangeAcronym.acronym == acronym).scalar()

    @staticmethod
    def lookup_by_acronym_or_code(acronym_or_code: str, session: model.Session):
        exchange = Exchange.lookup_by_acronym(acronym_or_code, session)
        if exchange:
            return exchange
        else:
            return Exchange.lookup_by_code(acronym_or_code, session)


class ExchangeAcronym(model.Base):
    __tablename__ = 'exchange_acronyms'
    operating_mic = Column(String(4), ForeignKey("exchanges.operating_mic"))
    acronym = Column(String(30), nullable=False)
    PrimaryKeyConstraint(operating_mic, acronym)
