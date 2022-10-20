from sqlalchemy import Column, DateTime, ForeignKey, FetchedValue, Table

import model

earnings_report_symbol_association = Table(
    'earnings_reports_symbols',
    model.Base.metadata,
    Column("id_symbol", ForeignKey("symbols.id"), primary_key=True),
    Column("id_earnings_report", ForeignKey("earnings_reports.id"), primary_key=True),
    Column("created", DateTime(timezone=True), FetchedValue())
)
