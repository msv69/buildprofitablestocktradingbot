from datetime import datetime
from strategies.isolation_strategy import IsolationStrategy
from tools.backtesting_tools import backtesting_engine


"""
    Script for backtesting strategies
"""

if __name__ == '__main__':
    # Run backtesting engine
    backtesting_engine(
        'TICKER', IsolationStrategy, args='DATA.csv',
        fromdate=datetime(2018, 1, 1), todate=datetime(2019, 1, 1)
    )