# models.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_squared_error, r2_score


def run_models(df, ticker):

    # =========================
    # PREPARE DATA
    # =========================

    features = df[['Open', 'High', 'Low', 'Volume']][:-1]

    target = df['Close'][1:]

    # =========================
    # TRAIN TEST SPLIT
    # =========================

    split_index = int(len(features) * 0.8)

    X_train = features[:split_index]

    X_test = features[split_index:]

    y_train = target[:split_index]

    y_test = target[split_index:]

    # =========================
    # MODELS
    # =========================

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=42),
        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
    }

    # =========================
    # RUN ALL MODELS
    # =========================

    for name, model in models.items():

        st.subheader(name)

        # Train
        model.fit(X_train, y_train)

        # Predict
        predictions = model.predict(X_test)

        # Metrics
        mse = mean_squared_error(y_test, predictions)

        r2 = r2_score(y_test, predictions)

        # Display Metrics
        col1, col2 = st.columns(2)

        col1.metric("MSE", round(mse, 2))

        col2.metric("R² Score", round(r2, 4))

        # =========================
        # GRAPH
        # =========================

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(
            y_test.values,
            label="Actual"
        )

        ax.plot(
            predictions,
            linestyle="--",
            label="Predicted"
        )

        ax.set_title(f"{ticker} - {name}")

        ax.legend()

        st.pyplot(fig)

    st.success("Prediction Completed Successfully ✅")