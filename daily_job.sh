#!/bin/zsh

echo "Usi tut?"

TARIEL_PATH=${0:a:h}
cd $TARIEL_PATH
PYTHONPATH=$PYTHONPATH:$TARIEL_PATH/loaders:$TARIEL_PATH/model:$TARIEL_PATH/utils:$TARIEL_PATH/providers:$TARIEL_PATH/config
export PYTHONPATH
venv/bin/python loaders/symbols_from_polygon.py >> /tmp/test.out 2>>/tmp/test.err
venv/bin/python loaders/dividends_from_polygon.py >> /tmp/test.out 2>>/tmp/test.err
venv/bin/python loaders/splits_from_polygon.py >> /tmp/test.out 2>>/tmp/test.err
venv/bin/python loaders/earnings_reports_from_twitter.py Livesquawk >> /tmp/test.out 2>>/tmp/test.err
venv/bin/python loaders/earnings_reports_from_twitter.py Marketcurrents >> /tmp/test.out 2>>/tmp/test.err