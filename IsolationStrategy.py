from models.isolation_model import IsolationModel
import backtrader as bt
import pandas as pd
import numpy as np


class IsolationStrategy(bt.Strategy):
    '''
        Explanation:
        The isolation forest identifies what it deems to be anomalies,
        overbought or oversold opportunities for entry. I append known data
        after fitting the isolation forest for the next day, making it an
        online unsupervised learningalgorithm.

        Current Issue: Positioning, Sizing, Exposure
'''

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self, data):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.dataclose = self.datas[0].close
        self.datavolume = self.datas[0].volume
        self.model_data = pd.read_csv(data)
        self.buyOut = False
        self.sellOut = False
        self.orderPosition = 0
        self.cooldown = 7

    # This is the code that gets copied into the trading system
    def next(self):
        self.log(self.dataclose[0])

        # Construct dataframe to predict
        x = pd.DataFrame(
            data=[[
                self.dataopen[0], self.datahigh[0], self.datalow[0],
                self.dataclose[0], self.datavolume[0]
                ]], columns='Open High Low Close Volume'.split()
        )

        # Create the model with all known data for normalization
        model = IsolationModel(self.model_data)

        # Append today's data for tomorrow's normalization
        self.model_data = self.model_data.append(x, ignore_index=True)

        # Dataframe to help normalize x
        mean_to_normalize = pd.DataFrame(data=[[
            np.mean(self.model_data['Open']), np.mean(self.model_data['High']),
            np.mean(self.model_data['Low']), np.mean(self.model_data['Close']),
            np.mean(self.model_data['Volume'])
            ]], columns='Open High Low Close Volume'.split())

        # Dataframe to help normalize x
        std_to_normalize = pd.DataFrame(data=[[
            np.std(self.model_data['Open']), np.std(self.model_data['High']),
            np.std(self.model_data['Low']), np.std(self.model_data['Close']),
            np.std(self.model_data['Volume'])
            ]], columns='Open High Low Close Volume'.split())

        # x is normalized as a parameter
        normalized_x = (x - mean_to_normalize) / std_to_normalize

        """
        # Write updated Data to CSV - To be included in the live system
        self.model_data.to_csv('FB.csv', index=False)
        """

        # Same but opposite conditions
        if model.predict_outlier(normalized_x) == -1 & \
                (self.dataclose[0] > np.mean(self.model_data['Close'])):
            self.log('SELL CREATE, %.2f' % self.dataclose[0])
            if not self.orderPosition == 0:
                self.sell(size=1)
                self.orderPosition -= 1

        # Same but opposite conditions
        if model.predict_outlier(normalized_x) == -1 & \
                (self.dataclose[0] < np.mean(self.model_data['Close'])) & \
                (self.cooldown == 0):
            self.log('BUY CREATE, %.2f' % self.dataclose[0])
            self.buy(size=1)
            self.orderPosition += 1
            self.cooldown = 7
        if self.cooldown > 0:
            self.cooldown -= 1