# visuals.py

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st


def close_price_chart(df, ticker):

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df['Date'], df['Close'])

    ax.set_title(f"{ticker} Closing Price")

    st.pyplot(fig)


def moving_average_chart(df, ticker):

    df['MA10'] = df['Close'].rolling(10).mean()

    df['MA50'] = df['Close'].rolling(50).mean()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(df['Date'], df['Close'], label='Close')

    ax.plot(df['Date'], df['MA10'], label='MA10')

    ax.plot(df['Date'], df['MA50'], label='MA50')

    ax.legend()

    ax.set_title(f"{ticker} Moving Averages")

    st.pyplot(fig)


def correlation_heatmap(df):

    numeric_df = df.select_dtypes(include='number')

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)

    st.pyplot(fig)


def interactive_chart(df, ticker):

    fig = px.line(
        df,
        x='Date',
        y='Close',
        title=f'{ticker} Interactive Trend'
    )

    st.plotly_chart(fig, use_container_width=True)