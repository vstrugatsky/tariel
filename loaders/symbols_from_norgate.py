from __future__ import annotations
from datetime import datetime
import csv

import model
from loaders.loader_base import LoaderBase
from model.jobs import Provider, JobType
from model.symbols_norgate import SymbolNorgate

class LoadSymbolsFromNorgate(LoaderBase):

    @staticmethod
    def load(csv_file_path: str, commit: bool):

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                symbol = SymbolNorgate()
                symbol.symbol = row[0] 
                symbol.name = row[1]  
                symbol.exchange = row[2]

                symbol_parts = symbol.symbol.split('-')
                if len(symbol_parts) == 2:
                    delisted_yymm = symbol_parts[1]
                    symbol.delisted = datetime.strptime(delisted_yymm, '%Y%m').date()
                with model.Session() as session:
                    session.merge(symbol)
                    if commit:
                        session.commit()


if __name__ == '__main__':
    commit = True
    loader = LoadSymbolsFromNorgate()
    loader.job_id = LoaderBase.start_job(provider=Provider.Norgate, job_type=JobType.Symbols, params='commit: ' + str(commit))
    loader.load("/Volumes/[C] Windows 11/NDExport/@HistoricalStockUniverse/names.txt", commit) 
    LoaderBase.finish_job(loader)
