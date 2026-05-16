# app.py

import streamlit as st
import pandas as pd
from datetime import date, timedelta

# =========================
# IMPORT CUSTOM MODULES
# =========================
from utils import (
    load_stock_data,
    calculate_statistics,
    risk_metrics,
    get_company_info
)

from visuals import (
    close_price_chart,
    moving_average_chart,
    correlation_heatmap,
    interactive_chart
)

from models import run_models


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="StellarStocks Predictor",
    page_icon="📈",
    layout="wide"
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📊 StellarStocks Predictor")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Analysis",
        "Prediction",
        "Visualization",
        "About"
    ]
)

# =========================
# HOME PAGE
# =========================
if page == "Home":

    st.title("📈 StellarStocks Predictor")

    st.markdown("""
    ### AI Powered Stock Market Analysis & Prediction

    Professional dashboard for:
    - Real-time Market Analysis
    - Machine Learning Predictions
    - Risk Assessment
    - Interactive Visualizations
    - Portfolio Comparison
    """)

    st.divider()

    # =========================
    # LIVE STOCK TRACKER
    # =========================

    st.subheader("📊 Live Stock Tracker")

    live_col1, live_col2 = st.columns([2, 1])

    with live_col1:

        live_ticker = st.text_input(
            "Search Stock Symbol",
            value="AAPL",
            key="live_tracker"
        )

    with live_col2:

        st.write("")

    try:

        live_df = load_stock_data(
            live_ticker,
            date.today() - timedelta(days=30),
            date.today()
        )

        if not live_df.empty:

            latest_price = round(
                live_df['Close'].iloc[-1],
                2
            )

            previous_price = round(
                live_df['Close'].iloc[-2],
                2
            )

            price_change = round(
                latest_price - previous_price,
                2
            )

            percent_change = round(
                (price_change / previous_price) * 100,
                2
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Current Price",
                f"${latest_price}"
            )

            c2.metric(
                "Daily Change",
                f"{price_change}"
            )

            c3.metric(
                "Change %",
                f"{percent_change}%"
            )

            interactive_chart(live_df, live_ticker)

    except:
        st.warning("Unable to fetch live stock data.")

    st.divider()

    # =========================
    # MULTI COMPANY COMPARISON
    # =========================

    st.subheader("📈 Multi Company Comparison")

    compare_tickers = st.text_input(
        "Enter Multiple Companies",
        value="AAPL,MSFT,GOOGL"
    )

    if st.button("Compare Companies"):

        import plotly.express as px
        import pandas as pd

        ticker_list = [
            t.strip().upper()
            for t in compare_tickers.split(",")
        ]

        compare_df = pd.DataFrame()

        for ticker in ticker_list:

            temp_df = load_stock_data(
                ticker,
                date.today() - timedelta(days=180),
                date.today()
            )

            if not temp_df.empty:

                temp_df['Ticker'] = ticker

                compare_df = pd.concat(
                    [compare_df, temp_df]
                )

        if not compare_df.empty:

            fig = px.line(
                compare_df,
                x='Date',
                y='Close',
                color='Ticker',
                title="Company Stock Comparison"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    st.info(
        "Built using Streamlit, Machine Learning & Yahoo Finance API."
    )


# =========================
# ANALYSIS PAGE
# =========================
elif page == "Analysis":

    st.title("📊 Stock Analysis")

    ticker = st.text_input("Enter Stock Symbol", "AAPL")

    start = st.date_input(
        "Start Date",
        value=date.today() - timedelta(days=365)
    )

    end = st.date_input(
        "End Date",
        value=date.today()
    )

    if st.button("Analyze Stock"):

        df = load_stock_data(ticker, start, end)

        if not df.empty:

            st.subheader("Stock Data")
            st.dataframe(df)

            # DOWNLOAD CSV
            csv = df.to_csv(index=False).encode()

            st.download_button(
                "⬇ Download CSV",
                csv,
                file_name=f"{ticker}_data.csv",
                mime="text/csv"
            )

            # COMPANY INFO
            st.subheader("🏢 Company Information")

            info = get_company_info(ticker)

            if info:

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Company Name:**", info["Name"])
                    st.write("**Sector:**", info["Sector"])
                    st.write("**Industry:**", info["Industry"])

                with col2:
                    st.write("**Country:**", info["Country"])
                    st.write("**Current Price:**", info["Current Price"])
                    st.write("**Market Cap:**", info["Market Cap"])

            # STATISTICS
            st.subheader("📈 Statistical Analysis")

            stats = calculate_statistics(df)

            stat1, stat2, stat3 = st.columns(3)

            stat1.metric("Mean Close", stats["Mean Close"])
            stat2.metric("Median Close", stats["Median Close"])
            stat3.metric("Std Deviation", stats["Standard Deviation"])

            # RISK METRICS
            st.subheader("⚠ Risk Metrics")

            risk = risk_metrics(df)

            r1, r2 = st.columns(2)

            r1.metric("Volatility", risk["Volatility"])
            r2.metric("Sharpe Ratio", risk["Sharpe Ratio"])

            # CHARTS
            st.subheader("📉 Closing Price Trend")
            close_price_chart(df, ticker)

            st.subheader("📊 Moving Averages")
            moving_average_chart(df, ticker)

            st.subheader("🔥 Correlation Heatmap")
            correlation_heatmap(df)


# =========================
# PREDICTION PAGE
# =========================
elif page == "Prediction":

    st.title("🤖 ML Stock Prediction")

    ticker = st.text_input(
        "Enter Stock Symbol",
        "AAPL",
        key="pred"
    )

    start = st.date_input(
        "Start Date",
        value=date.today() - timedelta(days=365),
        key="pred_start"
    )

    end = st.date_input(
        "End Date",
        value=date.today(),
        key="pred_end"
    )

    if st.button("Run Prediction"):

        df = load_stock_data(ticker, start, end)

        if not df.empty:

            run_models(df, ticker)


# =========================
# VISUALIZATION PAGE
# =========================
elif page == "Visualization":

    st.title("📈 Interactive Visualization")

    ticker = st.text_input(
        "Enter Stock Symbol",
        "AAPL",
        key="viz"
    )

    start = st.date_input(
        "Start Date",
        value=date.today() - timedelta(days=365),
        key="viz_start"
    )

    end = st.date_input(
        "End Date",
        value=date.today(),
        key="viz_end"
    )

    if st.button("Generate Visualization"):

        df = load_stock_data(ticker, start, end)

        if not df.empty:

            interactive_chart(df, ticker)


# =========================
# ABOUT PAGE
# =========================
if page == "About":

    st.header("ℹ️ About StellarStocks Predictor")

    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#111827,#1f2937);
        padding:30px;
        border-radius:18px;
        border:1px solid #374151;
        box-shadow:0 0 20px rgba(0,0,0,0.35);
        color:white;
    ">

    <h2 style="color:#38bdf8;">📈 StellarStocks Predictor</h2>

    <p style="font-size:17px; line-height:1.8; color:#d1d5db;">

    <b>StellarStocks Predictor</b> is a modern AI-powered stock market analysis and forecasting platform 
    developed to provide investors, analysts, and learners with intelligent market insights through 
    interactive visualizations, statistical analytics, and machine learning prediction models.

    <br><br>

    This platform combines real-time financial market data with advanced data science techniques 
    to help users explore stock trends, compare companies, evaluate risks, and understand future 
    market possibilities using predictive analytics.

    <br><br>

    The project is designed with a strong focus on:
    </p>

    <ul style="font-size:16px; line-height:2; color:#e5e7eb;">
        <li>✔️ Real-time stock market data analysis</li>
        <li>✔️ Machine Learning based forecasting models</li>
        <li>✔️ Interactive financial dashboards</li>
        <li>✔️ Portfolio and peer company comparison</li>
        <li>✔️ Risk analysis using volatility & statistical metrics</li>
        <li>✔️ User-friendly modern UI/UX experience</li>
        <li>✔️ Downloadable reports and visual analytics</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚀 Core Technologies Used")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="
            background:#111827;
            padding:20px;
            border-radius:15px;
            border-left:5px solid #38bdf8;
        ">
        <h4 style="color:#38bdf8;">🧠 Machine Learning</h4>

        - Linear Regression  
        - Decision Tree Regressor  
        - Random Forest Regressor  
        - Predictive Analytics  
        - Statistical Forecasting  

        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background:#111827;
            padding:20px;
            border-radius:15px;
            border-left:5px solid #22c55e;
        ">
        <h4 style="color:#22c55e;">📊 Data Visualization</h4>

        - Plotly Interactive Charts  
        - Seaborn Heatmaps  
        - Trend Analysis  
        - Moving Averages  
        - Portfolio Comparison  

        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background:#111827;
            padding:20px;
            border-radius:15px;
            border-left:5px solid #f59e0b;
        ">
        <h4 style="color:#f59e0b;">⚙️ Development Stack</h4>

        - Python  
        - Streamlit  
        - yFinance API  
        - Pandas & NumPy  
        - Scikit-learn  

        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    ### 💡 Project Highlights

    ✅ Real-time stock market tracking  
    ✅ AI-driven future stock price prediction  
    ✅ Interactive candlestick & trend charts  
    ✅ Risk assessment and volatility insights  
    ✅ Multi-company portfolio comparison  
    ✅ Downloadable CSV reports & visual graphs  
    ✅ Professional dashboard interface  
    ✅ Responsive and user-friendly design  
    """)

    st.markdown("---")

    st.markdown("""
    ### 👨‍💻 Developer

    <div style="
        background:#0f172a;
        padding:25px;
        border-radius:18px;
        border:1px solid #334155;
    ">

    <h3 style="color:#38bdf8;">Sajid Basha</h3>

    <p style="font-size:16px; line-height:1.9; color:#d1d5db;">

    Passionate Data Science student and developer focused on building 
    intelligent financial analytics systems using Artificial Intelligence, 
    Machine Learning, and modern visualization technologies.

    <br><br>

    This project reflects strong practical knowledge in:
    
    </p>

    <ul style="font-size:16px; line-height:2; color:#e5e7eb;">
        <li>✔️ Data Analysis & Financial Forecasting</li>
        <li>✔️ Machine Learning Model Development</li>
        <li>✔️ Backend Logic & API Integration</li>
        <li>✔️ Interactive Dashboard Development</li>
        <li>✔️ Real-time Data Processing</li>
        <li>✔️ UI/UX Design for Analytical Platforms</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.success("""
    StellarStocks Predictor demonstrates the practical application of 
    Data Science and Machine Learning in financial market analysis, 
    combining technical implementation with professional dashboard design 
    to create a complete intelligent analytics platform.
    """)

    st.warning("""
    ⚠️ Disclaimer:
    
    This project is developed for educational, analytical, and demonstration purposes only.
    Stock market predictions are based on historical data and machine learning models,
    which cannot guarantee future market performance.
    
    This should not be considered financial advice.
    """)