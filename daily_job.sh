#!/bin/zsh

TARIEL_PATH=`pwd`

PYTHONPATH=$PYTHONPATH:$TARIEL_PATH/loaders:$TARIEL_PATH/model:$TARIEL_PATH/utils:$TARIEL_PATH/providers:$TARIEL_PATH:/config
echo "PYTHONPATH" $PYTHONPATH
export PYTHONPATH
$TARIEL_PATH/venv/bin/python loaders/symbols_from_polygon.py
$TARIEL_PATH/venv/bin/python loaders/dividends_from_polygon.py
$TARIEL_PATH/venv/bin/python loaders/splits_from_polygon.py
$TARIEL_PATH/venv/bin/python loaders/earnings_reports_from_twitter.py Livesquawk
$TARIEL_PATH/venv/bin/python loaders/earnings_reports_from_twitter.py Marketcurrents