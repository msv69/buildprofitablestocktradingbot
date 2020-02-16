import backtrader as bt
import pyfolio as pf


def backtesting_engine(symbol, strategy, fromdate, todate, args=None):
    """
        Primary function for backtesting, not entirely parameterized
    """

    # Backtesting Engine
    cerebro = bt.Cerebro()

    # Add a Strategy if no Data Required for the model
    if args is None:
        cerebro.addstrategy(strategy)
    # If the Strategy requires a Model and therefore data
    elif args is not None:
        cerebro.addstrategy(strategy, args)

    # Retrieve Data from Alpaca
    data = bt.feeds.YahooFinanceData(
        dataname=symbol,
        fromdate=fromdate,  # datetime.date(2015, 1, 1)
        todate=todate,  # datetime.datetime(2016, 1, 1)
        reverse=False
    )

    # Add Data to Backtesting Engine
    cerebro.adddata(data)

    # Set Initial Portfolio Value
    cerebro.broker.setcash(100000.0)

    # Add Analysis Tools
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.PositionsValue, _name='posval')
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

    # Starting Portfolio Value
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run the Backtesting Engine
    backtest = cerebro.run()

    # Print Analysis and Final Portfolio Value
    print(
        'Final Portfolio Value: %.2f' % cerebro.broker.getvalue()
        )
    print(
        'Return: ', backtest[0].analyzers.returns.get_analysis()
        )
    print(
        'Sharpe Ratio: ', backtest[0].analyzers.sharpe.get_analysis()
        )
    print(
        'System Quality Number: ', backtest[0].analyzers.sqn.get_analysis()
        )
    print(
        'Drawdown: ', backtest[0].analyzers.drawdown.get_analysis()
        )
    print(
        'Active Position Value: ', backtest[0].analyzers.posval.get_analysis()
    )
    print(
        'Pyfolio: ', backtest[0].analyzers.pyfolio.get_analysis()
    )

    # Print Analysis and Final Portfolio Value
    pyfoliozer = backtest[0].analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()

    # See if we can add regular FB data to compare against returns of algo
    pf.create_full_tear_sheet(
        returns, positions=positions, transactions=transactions
        )


# TODO: Create pipeline: Optimization -> Testing essentially
class BacktestingPipeline:
    """
        Pipeline for in sample optimization and out of sample testing
    """
    pass