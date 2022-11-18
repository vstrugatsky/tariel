from sqlalchemy import Column, DateTime, ForeignKey, FetchedValue, Table

import model

event_symbol_association = Table(
    'event_symbols',
    model.Base.metadata,
    Column("id_symbol", ForeignKey("symbols.id"), primary_key=True),
    Column("id_event", ForeignKey("events.id"), primary_key=True),
    Column("created", DateTime(timezone=True), FetchedValue())
)
