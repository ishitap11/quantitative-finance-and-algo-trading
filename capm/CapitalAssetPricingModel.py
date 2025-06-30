import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

class CapitalAssetPricingModel:
    def __init__(self, assets, start_date, end_date):
        self.data = None
        self.assets = assets
        self.start_date = start_date
        self.end_date = end_date

    def load_data(self):
        stock_data = {}
        for asset in self.assets:
            ticker = yf.Ticker(asset)
            stock_data[asset] = ticker.history(start=self.start_date, end=self.end_date)['Close']

        return pd.DataFrame(stock_data)

    def initialize_model(self):
        stock_data = self.load_data()
        #We want to use monthly returns instead of daily returns, so we just keep end of month close price. [See README]
        stock_data = stock_data.resample('ME').last()
        self.data = pd.DataFrame({'s_close': stock_data[self.assets[0]],
                                  'm_close': stock_data[self.assets[1]]})

        #logarithmic monthly returns similar to Markowitz Model to normalize the dataset
        self.data[['s_returns', 'm_returns']] = np.log(self.data[['s_close', 'm_close']] /
                                                   self.data[['s_close', 'm_close']].shift(1))
        self.data = self.data[1:]
        print(self.data)

    def calculate_beta_factor(self):
        cov_matrix = np.cov(self.data['s_returns'], self.data['m_returns'])
        beta = cov_matrix[0,1] / cov_matrix[1,1]
        print("beta is: ", beta)
        return beta



if __name__ == "__main__":
    capm = CapitalAssetPricingModel(['IBM', '^GSPC'], '2010-01-01', '2017-01-01' )
    capm.initialize_model()
    capm.calculate_beta_factor()