import requests
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

# Pick up companies from US Dow 30
url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
r = requests.get(url)
# Select table from wikipedia page.
df = pd.read_html(r.content,attrs = {'id': 'constituents'})[0]
# Select top 5 stocks from the table using the head function and sort by index weighting.
weighting_df = df.sort_values('Index weighting', ascending=False).head()
tickers = weighting_df['Symbol'].tolist()

# Form table that we will use to store our stock data.
maindf = pd.DataFrame([i for i in range(100)])

# Use AlphaVantage API to get stock information for each stock in tickers.
for i in range(len(tickers)):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&outputsize=compact&apikey=RUW3DFCH4DITUL4B".format(tickers[i])
    r = requests.get(url)
    # Following lines fix formatting issues from the AlphaVantage API
    data = r.json()
    data.pop("Meta Data")
    
    df2 = pd.DataFrame(data)
    df2 = pd.json_normalize(df2['Time Series (Daily)'])
    df2 = df2.drop(['1. open', '2. high', '3. low', '5. volume'], axis=1)
    df2 = df2.rename(columns={"4. close": "{}".format(tickers[i])})
    # Add closing stock price info from df2 and merge it into maindf
    maindf = pd.merge(maindf, df2, left_index=True, right_index=True)

# Get rid of any merged columns and make sure maindf values are floats.
maindf = maindf.iloc[: , 1:].astype(float)
corr_data = maindf.corr()

def myplot():
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(1,1,1)
    plt.title("Correlation Graph: US Dow 30 Top 5 Stocks", pad = 20)   
    heatmap = ax.pcolor(corr_data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(corr_data.shape[0]) + 0.5,minor = False)
    ax.set_yticks(np.arange(corr_data.shape[1]) + 0.5,minor = False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    column_labels = corr_data.columns
    row_labels = corr_data.index
       
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=0)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()


# Call plotting function.
myplot()




