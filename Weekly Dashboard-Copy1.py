#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install yfinance


# In[1]:


import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd


# In[2]:


def get_last_week_return(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    hist_data = ticker.history(period="1wk")
    last_week_return = (hist_data['Close'][-1] - hist_data['Open'][0]) / hist_data['Open'][0]
    return last_week_return


# In[3]:


def get_last_week_volatility(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    hist_data = ticker.history(period="1wk")
    daily_returns = hist_data['Close'].pct_change()
    weekly_volatility = daily_returns.std() * (5 ** 0.5)  # Multiply by square root of 5 for weekly volatility
    return weekly_volatility


# In[4]:


def get_monthly_returns(ticker_symbol, num_years):
    # Get historical data
    ticker = yf.Ticker(ticker_symbol)
    hist_data = ticker.history(period=f"{num_years}y")
    
    # Resample data to monthly frequency and calculate returns
    monthly_returns = hist_data['Close'].resample('M').ffill().pct_change()
    
    return monthly_returns


# In[15]:


def get_current_pe_ratio(index_symbol):
    index = yf.Ticker(index_symbol)
    pe_ratio = index.info.get('trailingPE', None)
    return pe_ratio


# In[24]:


# Function to fetch forward P/E ratio for a given stock
def get_forward_pe_ratio(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    # Get the latest stock price
    latest_price = stock.info.get('previousClose', None)
    # Get the estimated future earnings per share (EPS)
    estimated_eps = stock.info.get('forwardEps', None)
    if latest_price is not None and estimated_eps is not None and estimated_eps != 0:
        forward_pe_ratio = latest_price / estimated_eps
        return forward_pe_ratio
    else:
        return None


# In[5]:


# Ticker symbols for S&P 500 and Barclays Agg
spx_ticker = "^GSPC"  # S&P 500
bonds_ticker = "AGG"     # Barclays Agg
acwi_ticker = "ACWI"     #ACWI
treas_ticker = "^TNX"    #US 10 Year Treasury
gold_ticker = "GC=F"     #Gold
oil_ticker = "CL=F"      #Oil
usdeur_ticker = "USDEUR=X"  #USD EUR


# Get last week's returns
spx_last_week_return = get_last_week_return(spx_ticker)
bonds_last_week_return = get_last_week_return(bonds_ticker)
acwi_last_week_return = get_last_week_return(acwi_ticker)
treas_last_week_return = get_last_week_return(treas_ticker)
gold_last_week_return = get_last_week_return(gold_ticker)
oil_last_week_return = get_last_week_return(oil_ticker)
usdeur_last_week_return = get_last_week_return(usdeur_ticker)


spx_sharpe_ratio = get_last_week_return(spx_ticker)/get_last_week_volatility(spx_ticker)
bonds_sharpe_ratio = get_last_week_return(bonds_ticker)/get_last_week_volatility(bonds_ticker)
acwi_sharpe_ratio = get_last_week_return(acwi_ticker)/get_last_week_volatility(acwi_ticker)
treas_sharpe_ratio = get_last_week_return(treas_ticker)/get_last_week_volatility(treas_ticker)
gold_sharpe_ratio = get_last_week_return(gold_ticker)/get_last_week_volatility(gold_ticker)
oil_sharpe_ratio = get_last_week_return(oil_ticker)/get_last_week_volatility(oil_ticker)
usdeur_sharpe_ratio = get_last_week_return(usdeur_ticker)/get_last_week_volatility(usdeur_ticker)



# Plotting
fig, ax1 = plt.subplots(figsize=(8, 5))
bar_width = 0.35
bar_positions = [1, 2, 3, 4, 5, 6, 7]

bars_spx = ax1.bar(bar_positions[0], spx_last_week_return, bar_width, color='b')
bars_bonds = ax1.bar(bar_positions[1], bonds_last_week_return, bar_width, color='r')
bars_acwi = ax1.bar(bar_positions[2], acwi_last_week_return, bar_width, color='g')
bars_treas = ax1.bar(bar_positions[3], treas_last_week_return, bar_width, color='purple') 
bars_gold = ax1.bar(bar_positions[4], gold_last_week_return, bar_width, color='gold')
bars_oil = ax1.bar(bar_positions[5], oil_last_week_return, bar_width, color='grey')
bars_usdeur = ax1.bar(bar_positions[6], usdeur_last_week_return, bar_width, color='orange')


# Secondary y-axis (Sharpe ratio)
ax2 = ax1.twinx()
markers_spx = ax2.plot(bar_positions[0], spx_sharpe_ratio, 'kd', markersize=10)
markers_bonds = ax2.plot(bar_positions[1], bonds_sharpe_ratio, 'kd', markersize=10)
markers_acwi = ax2.plot(bar_positions[2], acwi_sharpe_ratio, 'kd', markersize=10)
markers_treas = ax2.plot(bar_positions[3], treas_sharpe_ratio, 'kd', markersize=10)
markers_gold = ax2.plot(bar_positions[4], gold_sharpe_ratio, 'kd', markersize=10)
markers_oil = ax2.plot(bar_positions[5], oil_sharpe_ratio, 'kd', markersize=10)
markers_usdeur = ax2.plot(bar_positions[6], usdeur_sharpe_ratio, 'kd', markersize=10)

ax2.set_ylabel('Risk Adjusted Returns')
ax1.set_ylabel('Total Returns')

ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f'))
ax1.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

plt.title('Past Week Returns')
plt.xlabel('Asset')


plt.xticks(bar_positions, ['S&P 500', 'Barclays Agg' , 'MSCI ACWI', 'US 10Yr' , 'Gold', 'Oil', 'USDEUR'])
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# In[6]:


#Box & Whisker Plot
spx_ticker = "^GSPC"  # S&P 500
tpx_ticker = "1475.T"   # Topix
stxx_ticker = "^STOXX"   # STOXX 600

# Number of years for historical data
num_years = 40

# Get weekly returns
spx_monthly_returns = get_monthly_returns(spx_ticker, num_years)
stxx_monthly_returns = get_monthly_returns(stxx_ticker, num_years)
tpx_monthly_returns = get_monthly_returns(tpx_ticker, num_years)

spx_monthlies = (spx_monthly_returns).values
stxx_monthlies = (stxx_monthly_returns).values
tpx_monthlies = (tpx_monthly_returns).values

spx_monthly_rets = spx_monthlies[~np.isnan(spx_monthlies)]
stxx_monthly_rets = stxx_monthlies[~np.isnan(stxx_monthlies)]
tpx_monthly_rets = tpx_monthlies[~np.isnan(tpx_monthlies)]


# Plotting box and whisker plot
plt.figure(figsize=(10,6))


plt.boxplot([spx_monthly_rets, stxx_monthly_rets, tpx_monthly_rets], positions =[1,2,3], showmeans=True, meanline=True, sym='b+', patch_artist=True, boxprops=dict(facecolor='lightblue'),showfliers=False)


x=[1,2,3]
labels = ['S&P 500', 'TOPIX', 'STOXX 600']
plt.xticks(x, labels, rotation ='horizontal') 

# Add a star marker for the past week's return
last_month_return_spx = spx_monthly_returns.iloc[-1]
last_month_return_stxx = stxx_monthly_returns.iloc[-1]
last_month_return_tpx = tpx_monthly_returns.iloc[-1]




plt.plot([1], last_month_return_spx, 'r*', markersize=10, label='Past Month Return')
plt.plot([2], last_month_return_stxx, 'r*', markersize=10 )
plt.plot([3], last_month_return_tpx, 'r*', markersize=10 )


plt.title('Equity Market Returns')
plt.ylabel('Monthly Returns')
plt.grid(True)
plt.legend()
plt.show()


# In[23]:


# Regional Valuations

etfs = {
    "TOPIX ETF": "1329.T",
    "S&P 500 ETF": "SPY",
    "STOXX 600 ETF": "EXSA.DE"
}

# Fetch current P/E ratios for ETFs
current_pe_ratios = {etf: get_current_pe_ratio(symbol) for etf, symbol in etfs.items()}

# Calculate historical average P/E ratios for ETFs
historical_average_pes = {etf: calculate_historical_pe_average(symbol) for etf, symbol in etfs.items()}

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Current P/E ratios
ax.bar(current_pe_ratios.keys(), current_pe_ratios.values(), color='skyblue', label='Current P/E Ratio')

# Historical average P/E ratios
ax.plot(historical_average_pes.keys(), historical_average_pes.values(), marker='o', linestyle='-', color='orange', label='Historical Average P/E Ratio')

# Add labels and title
ax.set_xlabel('Index ETF')
ax.set_ylabel('P/E Ratio')
ax.set_title('Current and Historical Average P/E Ratios for Major Index ETFs')
ax.legend()

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[26]:


stock_symbol = "SPY"  # Example: Apple Inc.
forward_pe_ratio = get_forward_pe_ratio(stock_symbol)
if forward_pe_ratio is not None:
    print(f"The forward P/E ratio for {stock_symbol} is: {forward_pe_ratio:.2f}")
else:
    print(f"Unable to fetch forward P/E ratio for {stock_symbol}.")


# In[ ]:


#


# In[ ]:




