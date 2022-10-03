import model as model
from model.symbols import Symbol
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Numeric, BigInteger, Date, ForeignKey, PrimaryKeyConstraint
from datetime import datetime
from providers.fmp import Fmp
import requests
from deprecated import deprecated


@deprecated("numbers not accurate")
class Estimate(model.Base):
    __tablename__ = 'estimates'
    symbol = Column(String(10), ForeignKey("symbols.symbol"))
    symbol_object = relationship("Symbol")
    period_end_date = Column(Date, nullable=False)

    estimated_revenue_low = Column(BigInteger)
    estimated_revenue_high = Column(BigInteger)
    estimated_revenue_avg = Column(BigInteger)
    estimated_ebitda_low = Column(BigInteger)
    estimated_ebitda_high = Column(BigInteger)
    estimated_ebitda_avg = Column(BigInteger)
    estimated_ebit_low = Column(BigInteger)
    estimated_ebit_high = Column(BigInteger)
    estimated_ebit_avg = Column(BigInteger)
    estimated_netincome_low = Column(BigInteger)
    estimated_netincome_high = Column(BigInteger)
    estimated_netincome_avg = Column(BigInteger)
    estimated_sgaexpense_low = Column(BigInteger)
    estimated_sgaexpense_high = Column(BigInteger)
    estimated_sgaexpense_avg = Column(BigInteger)
    estimated_eps_avg = Column(Numeric)
    estimated_eps_high = Column(Numeric)
    estimated_eps_low = Column(Numeric)
    number_analysts_estimated_revenue = Column(Numeric)
    number_analysts_estimated_eps = Column(Numeric)
    PrimaryKeyConstraint(symbol, period_end_date)

    @classmethod
    def from_fmp(cls, i):
        return cls(
            symbol=i.get('symbol'),
            period_end_date=i.get('date'),
            estimated_revenue_low=i.get('estimatedRevenueLow'),
            estimated_revenue_high=i.get('estimatedRevenueHigh'),
            estimated_revenue_avg=i.get('estimatedRevenueAvg'),
            estimated_ebitda_low=i.get('estimatedEbitdaLow'),
            estimated_ebitda_high=i.get('estimatedEbitdaHigh'),
            estimated_ebitda_avg=i.get('estimatedEbitdaAvg'),
            estimated_ebit_low=i.get('estimatedEbitLow'),
            estimated_ebit_high=i.get('estimatedEbitHigh'),
            estimated_ebit_avg=i.get('estimatedEbitAvg'),
            estimated_netincome_low=i.get('estimatedNetIncomeLow'),
            estimated_netincome_high=i.get('estimatedNetIncomeHigh'),
            estimated_netincome_avg=i.get('estimatedNetIncomeAvg'),
            estimated_sgaexpense_low=i.get('estimatedSgaExpenseLow'),
            estimated_sgaexpense_high=i.get('estimatedSgaExpenseHigh'),
            estimated_sgaexpense_avg=i.get('estimatedSgaExpenseAvg'),
            estimated_eps_avg=i.get('estimatedEpsAvg'),
            estimated_eps_high=i.get('estimatedEpsHigh'),
            estimated_eps_low=i.get('estimatedEpsLow'),
            number_analysts_estimated_revenue=i.get('numberAnalystEstimatedRevenue'),
            number_analysts_estimated_eps=i.get('numberAnalystsEstimatedEps'))

    @staticmethod
    def load_from_fmp(i):
        if model.Session().query(Symbol).filter(Symbol.symbol == i.get('ticker')):
            estimate = Estimate.from_fmp(i)
            return estimate
        else:
            print(f'WARN {datetime.utcnow()} {i.get("ticker")} not found in Symbols')
            return None

# data quality poor, does not match SeekingAlpha or Zacks
def load_from_fmp(symbol, payload, method):
    r = requests.get(Fmp.fmpPrefix + '/v3/analyst-estimates/' + symbol, params=payload)
    print(f'INFO {datetime.utcnow()} URL={r.url} \n Status={r.status_code}')

    session = model.Session()
    for i in r.json():
        print(i)
        model_object = method(i)
        if model_object:
            session.merge(model_object)
    session.commit()
    session.close()


if __name__ == '__main__':
    load_from_fmp('AAPL', {'apikey': Fmp.fmpApiKey, 'period': 'quarter'}, Estimate.load_from_fmp)
