# importing all the libraries that we require for Dashboard Visualisation

from newsapi import NewsApiClient
import streamlit as st
import pandas as pd
import numpy as np
from GoogleNews import GoogleNews
import sys
import yfinance as yf
import pandas_datareader.data as web
from pandas_datareader import wb
import datetime
import streamlit.components.v1 as components
from pivottablejs import pivot_ui
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


newsapi = NewsApiClient(api_key='b6c59bf93ef84bc28fcebe34b66ee639')
googlenews = GoogleNews()


st.sidebar.title('LinkTech Fund Management Analytics Portal')

# News Dashboard Selection
if st.sidebar.checkbox('News Search Dashboard'):

    value = st.selectbox(
        'Please Select the Search preference',
        ('Newsapi', 'Google Search'))

    if(value == 'Newsapi'):
        input = st.text_input(
            'Enter What you have to Search for', 'stock in news')
        top_headlines = newsapi.get_everything(q=str(input))
        for headline in top_headlines['articles']:
            st.write("Title : " + headline['title'])
            st.write("Description: " + headline['url'])
    elif(value == 'Google Search'):
        input = st.text_input(
            'Enter What you have to Search for', 'stock in news')
        googlenews.search(str(input))
        for results in googlenews.results():
            st.write("Title : " + results['title'])
            st.write("Description: " + results['desc'])
            st.write("Link: " + results['link'])
if st.sidebar.checkbox('Stocks Data Analysis'):
    st.write("Dashboard For Stock Analysis Using Python and Machine Learning")
    if st.checkbox("Search Value Stock"):
        st.write("Value Stocks")
        data = pd.read_csv("Recomm.csv")
        value = data[(data['EPS'] > 0) & (
            data['Value Indicator'] == 1) & (data['Sales_Growth'] > 0)
            & (data['Operating_Profit_Growth'] > 0) & (data['PE Ratio'] > 0)]

        st.dataframe(value)

    elif st.checkbox("Search Growth Stock"):
        st.write("Growth Stocks")
        data = pd.read_csv("Recomm.csv")
        growth = data[(data['EPS'] > 0) & (
            data['Growth Indicator'] == 1) & (data['Sales_Growth'] > 0)
            & (data['Operating_Profit_Growth'] > 0) & (data['PE Ratio'] > 0)]

        st.dataframe(growth)
    elif st.checkbox("Research"):
        val = st.text_input('Enter the Yahoo Finance Symbol', 'TCS.NS')
        stock = yf.Ticker(val)
        st.write(stock.info["longName"])

        if st.checkbox("Stock Info"):
            st.write(stock.info)
        elif st.checkbox("Price Charts"):
            st.write("Charts Diplay Section")
            i = st.sidebar.selectbox(
                "Interval in minutes", ("1d", "1m", "5m", "15m", "30m"))
            p = st.sidebar.number_input(
                "How many days (1-365)", min_value=1, max_value=365, step=1, value=365)
            data = stock.history(interval=i, period=str(p) + "d")
            fig = go.Figure(data=[go.Candlestick(x=data.index,
                                                 open=data['Open'],
                                                 high=data['High'],
                                                 low=data['Low'],
                                                 close=data['Close'])])

            st.plotly_chart(fig, use_container_width=True)
            if st.checkbox('Display Data in DataFrame'):
                st.dataframe(data)

        elif st.checkbox("Balance Sheet"):
            df = stock.balance_sheet

            data = df[(df.index == 'Total Assets')
                      | (df.index == 'Total Liab')]
            fig = px.bar(data.T, barmode='group')
            st.plotly_chart(fig, use_container_width=True)

            if st.checkbox('View All Data'):
                st.dataframe(df)

        elif st.checkbox(" Cash Flow"):
            st.dataframe(stock.cashflow)
        elif st.checkbox("Financials"):
            st.dataframe(stock.financials)
        elif st.checkbox("Major Institutional Holders"):
            st.write(stock.institutional_holders)
        elif st.checkbox("Analyst Recommendation"):
            st.write(stock.recommendations)
        elif st.checkbox("Earnings Report"):
            fig = px.bar(stock.earnings, barmode='group')
            st.plotly_chart(fig, use_container_width=True)
if st.sidebar.checkbox("Risk Management "):
    if st.checkbox(' Scenario Analysis'):
        col1, col2 = st.columns(2)
        price = col1.number_input(
            "Price of the Stock  You Bought", value=200.00)
        max_loss = col1.number_input(
            "Enter the amount of Loss you can withstand", value=2000)
        stop_loss = col1.number_input(
            "Enter the last price when you will exit the stock", value=price*0.95)
        price_target = col1.number_input(
            "Price of the Stock  You Bought", value=205.00)

        vol = max_loss/(price - stop_loss)
        st.write("Volume you can purchase = %s" % vol)
        profit0 = price*vol - price*vol
        stop = (stop_loss - price)*vol
        profit1 = (price_target-price)*vol

        df = pd.DataFrame({'Scenario': [profit1, profit0, stop], }, index=[
                          price_target, price, stop_loss])
        fig = px.line(df, x="Scenario")

        col1.plotly_chart(fig)
        if col2.checkbox("Value at Risk Parameters Check"):
            col2.write("Welcome to Risk Statistical Analysis Dashboard")


if st.sidebar.checkbox("Fed And World Bank Data Analysis"):
    if st.checkbox('FRED Data'):
        st.markdown('## Welcome To US Fed Data Analysis Section.')
        st.markdown(
            'Before Proceeding with your research their are some indicators that can help you.')
        st.markdown(
            '1. **Unemployment Rate (SYMBOl:UNRATE)** : This Indicator help us understand about how good is US economy doing.However, it is generally said that when unemployment rate drops stock markest do well and when unemployment rate increase the stock market crashes. However, some research suggest that its just one of the factors and hence should not be relied upon this data alone')
        start = st.date_input("Enter From Date", datetime.date(2009, 7, 6))
        end = st.date_input("Enter To Date", datetime.date(2022, 3, 3))
        symbol = st.text_input(
            "Please Enter the Symbol of the Data you want form FRED Site.", 'GDP')

        data = web.DataReader(str(symbol), 'fred', start, end)
        if st.checkbox('View Data'):
            st.write(data)
        st.line_chart(data)
    elif st.checkbox('World Bank Indicator'):
        search_input = st.text_input(
            'Enter What you Want to search on the world bank site', 'gdp.*capita.*const')
        matches = wb.search(str(search_input))
        st.write(matches)
        st.text('Download World Bank Data')
        star = st.date_input("Enter From Date", datetime.date(2009, 7, 6))
        en = st.date_input("Enter To Date", datetime.date(2022, 3, 3))
        count = st.text_input('Enter the Country Symbol', 'US')
        symbol = st.text_input('Enter the indicator symbol', 'NY.GDP.PCAP.KD')

        data = wb.download(indicator=str(symbol),
                           country=str(count), start=star, end=en)
        st.write(data)
