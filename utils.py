# utils.py

import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import date


# ==============================
# LOAD STOCK DATA
# ==============================
def load_stock_data(ticker, start, end):

    try:
        df = yf.download(
            ticker,
            start=start,
            end=end,
            progress=False
        )

        # Empty dataframe check
        if df.empty:
            st.error("No data found for this stock symbol.")
            return pd.DataFrame()

        # Reset index
        df.reset_index(inplace=True)

        # ==============================
        # FIX MULTIINDEX COLUMNS
        # ==============================
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        # Keep only required columns
        needed_cols = [
            'Date',
            'Open',
            'High',
            'Low',
            'Close',
            'Volume'
        ]

        df = df[needed_cols]

        # Convert numeric columns safely
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop null rows
        df.dropna(inplace=True)

        return df

    except Exception as e:
        st.error(f"Error loading stock data: {e}")
        return pd.DataFrame()


# ==============================
# BASIC STOCK STATISTICS
# ==============================
def calculate_statistics(df):

    stats = {
        "Mean Close": round(df['Close'].mean(), 2),
        "Median Close": round(df['Close'].median(), 2),
        "Maximum Close": round(df['Close'].max(), 2),
        "Minimum Close": round(df['Close'].min(), 2),
        "Standard Deviation": round(df['Close'].std(), 2),
        "Variance": round(df['Close'].var(), 2)
    }

    return stats


# ==============================
# DAILY RETURNS
# ==============================
def calculate_returns(df):

    df['Daily Return'] = df['Close'].pct_change()

    return df


# ==============================
# RISK METRICS
# ==============================
def risk_metrics(df):

    df = calculate_returns(df)

    volatility = df['Daily Return'].std() * (252 ** 0.5)

    sharpe_ratio = (
        df['Daily Return'].mean() / df['Daily Return'].std()
    ) * (252 ** 0.5)

    return {
        "Volatility": round(volatility, 4),
        "Sharpe Ratio": round(sharpe_ratio, 4)
    }


# ==============================
# DATE VALIDATION
# ==============================
def validate_dates(start, end):

    if start > end:
        st.error("Start date cannot be after end date.")
        return False

    if end > date.today():
        st.warning("End date adjusted to today.")

    return True


# ==============================
# COMPANY INFO
# ==============================
def get_company_info(ticker):

    try:
        stock = yf.Ticker(ticker)

        info = stock.info

        company_data = {
            "Name": info.get("longName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Country": info.get("country", "N/A"),
            "Website": info.get("website", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "Current Price": info.get("currentPrice", "N/A")
        }

        return company_data

    except:
        return None