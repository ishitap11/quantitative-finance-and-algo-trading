import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as opt

#average number of trading days in a year
NUM_TRADING_DAYS = 252
NUM_PORTFOLIOS = 10000
# defining the stock names for the universe
stocks = ['AAPL', 'AMZN', 'GE', 'DB', 'TSLA', 'WMT']

# Date range for the analysis
start_date = '2012-01-01'
end_date = '2017-01-01'

def download_data():
    # dictionary of stock name (key) - closing prices of each day (values)
    stock_data = {}
    for stock in stocks:
        ticker = yf.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date, end=end_date)['Close']

    return pd.DataFrame(stock_data)

def show_data(data):
    data.plot(figsize=(10, 5))
    plt.show()

def calculate_return(data):
    #Natural Log helps normalize the dataset since each stock has different volatility
    log_return = np.log(data/data.shift(1)) #S(t+1)/S(t)
    # the data.shift(n) function shifts the array of values by n places. so value at data[k] --> data[k+n]
    return log_return[1:] #leave out row 0 as it will be not defined since S[-1] does not exist

def show_statistics(returns):
    #gives mean annual return = daily mean * number of trading days
    print(returns.mean()*NUM_TRADING_DAYS)
    #covariance matrix
    print(returns.cov()*NUM_TRADING_DAYS)

def get_expected_mean(returns, weights):
    return np.sum(returns.mean() * weights) * NUM_TRADING_DAYS

def get_expected_risk(returns, weights):
    return np.sqrt(np.dot(weights.T, np.dot(returns.cov()*NUM_TRADING_DAYS, weights)))

def show_expected_mean_variance(returns, weights):
    # expected return
    portfolio_returns = get_expected_mean(returns, weights)
    print("expected return of portfolio: ", portfolio_returns)
    # expected risk using covariance
    portfolio_volatility_risk = get_expected_risk(returns, weights)
    print("expected volatility of portfolio: ", portfolio_volatility_risk)

def statistics(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * NUM_TRADING_DAYS, weights)))
    return np.array([portfolio_return, portfolio_volatility,
                     portfolio_return / portfolio_volatility])


#Returns the sharpe ratio function as -f(x) that can be optimised
def min_function_sharpe(weights, returns):
    return -statistics(weights, returns)[2]


# we need to define the following for the scipy.optimize()
# constraints to be applied on 'x' being optimised --> here weights
# bounds for each value of 'x'
# optimisation method used SLSQP --> see documentation for details
def optimise_portfolio(returns, weights):
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(len(stocks)))
    return opt.minimize(fun=min_function_sharpe, x0=weights[0], args=returns
                                 , method='SLSQP', bounds=bounds, constraints=constraints)

def generate_portfolio(returns):
    portfolio_weights = []
    portfolio_returns = []
    portfolio_volatility_risk = []

    for _ in range(NUM_PORTFOLIOS):
        weights = np.random.random(len(stocks))
        weights /= np.sum(weights) # make sure weights add up to 1 (100%)
        portfolio_weights.append(weights)
        #expected return for each portfolio
        portfolio_returns.append(get_expected_mean(returns, weights))
        #expected risk for each portfolio
        portfolio_volatility_risk.append(get_expected_risk(returns, weights))

    return np.array(portfolio_weights), np.array(portfolio_returns), np.array(portfolio_volatility_risk)

def show_portfolio(returns, volatility_risk):
    plt.figure(figsize=(10, 6))
    plt.scatter(volatility_risk, returns, c=returns/volatility_risk, marker='o') #c --> color based on sharpe ratio
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')

def print_optimal_portfolio(optimum, returns):
    print("Optimal portfolio: ", optimum['x'].round(3))
    print("Expected return, volatility and Sharpe ratio: ",
          statistics(optimum['x'].round(3), returns))

def show_optimal_portfolio(opt, rets, portfolio_rets, portfolio_vols):
    plt.figure(figsize=(10, 6))
    plt.scatter(portfolio_vols, portfolio_rets, c=portfolio_rets / portfolio_vols, marker='o')
    plt.grid(True)
    plt.xlabel('Expected Volatility')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.plot(statistics(opt['x'], rets)[1], statistics(opt['x'], rets)[0], 'g*', markersize=20.0)
    plt.show()

if __name__ == "__main__":
    data = download_data()
    show_data(data)
    daily_returns = calculate_return(data)
    portfolio_weights, return_means, volatility_risk = generate_portfolio(daily_returns)
    show_portfolio(return_means, volatility_risk)
    optimal = optimise_portfolio(daily_returns, portfolio_weights)
    print_optimal_portfolio(optimal, daily_returns)
    show_optimal_portfolio(optimal, daily_returns, return_means, volatility_risk)