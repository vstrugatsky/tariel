#!/bin/zsh

TARIEL=${0:a:h}
cd "$TARIEL" || exit

start=$(date +%s)  # seconds since epoch
echo "STARTTIME: $start" >> /tmp/test.out

PYTHONPATH=$PYTHONPATH:$TARIEL/loaders:$TARIEL/model:$TARIEL/utils:$TARIEL/providers:$TARIEL/config:$TARIEL/reports
export PYTHONPATH

{
venv/bin/python loaders/symbols_from_polygon.py
venv/bin/python loaders/dividends_from_polygon.py
venv/bin/python loaders/splits_from_polygon.py
venv/bin/python loaders/earnings_reports_from_twitter.py Livesquawk
venv/bin/python loaders/earnings_reports_from_twitter.py Marketcurrents

venv/bin/python reports/daily_jobs_email.py "$start"
} >> /tmp/test.out 2>>/tmp/test.err