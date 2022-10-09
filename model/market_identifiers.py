import model as model
from sqlalchemy import Column, String, Text, ForeignKey, PrimaryKeyConstraint


class MarketIdentifier(model.Base):
    __tablename__ = 'market_identifier_codes_iso_10383'
    mic = Column(String(4), primary_key=True)
    operating_mic = Column(String(4), nullable=False)

    @staticmethod
    def lookup_operating_mic_by_mic(mic: str, session: model.Session):
        return session.query(MarketIdentifier.operating_mic).filter(MarketIdentifier.mic == mic).scalar()

