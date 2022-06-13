import streamlit as st
import datetime as dt
from prophet import Prophet
import pandas as pd

def forecast():
    query_df = pd.read_csv(st.session_state['uploaded_file'] )
    st.header('**Forecasting**')
    with st.container():
        ds_selection = st.selectbox("Select a date column", query_df.columns)
        # create 3 containers for the forecasting area
        container1_col1, container1_col2, container1_col3 = st.columns(3)
        # Container 1: select the frequency
        with container1_col1:
            freq = st.selectbox(
                "Is the data period monthly or daily?", ("Monthly", "Weekly", "Daily"))
        # Container 2: select the number of periods
        with container1_col2:
            period = st.number_input(
                "Number of periods to forecast", value=1, min_value=1, max_value=365)
        # Container 3: select the seasonality mode
        with container1_col3:
            seasonality = st.selectbox(
                "Seasonality Mode", ("additive", "multiplicative"))
    with st.container():
        container2_col1, container2_col2 = st.columns(2)
        with container2_col1:
            changepoint_prior_scale = st.slider(
                "changepoint_prior_scale", 0.01, 0.99, 0.05)
        with container2_col2:
            changepoint_range = st.slider(
                "changepoint_range", 0.01, 0.99, 0.05)
    if freq == "Monthly":
        freq = "MS"
    elif freq == "Weekly":
        freq = "W"
    else:
        freq = "D"
    y = st.selectbox(
        "Select a target column (it must be numeric)", query_df.columns, index=1)
    if st.button("Forecast"):
        with st.spinner('Forecasting...'):
            ds = query_df[ds_selection]
            # group ds by index and sum
            #ds = ds.groupby(ds.index).sum()
            y = query_df[y]
            # cast y to int
            y = y.astype(int)
            df = pd.DataFrame({'ds': ds, 'y': y})
            df = df.groupby('ds').agg('sum')
            df = df.reset_index()
            st.write(df)
            today = dt.datetime.today()
            today = pd.to_datetime(today)
            today = today.strftime('%Y-%m-%d')
            df = df.query('ds <= @today')
            m = Prophet(seasonality_mode=seasonality,
                        changepoint_prior_scale=changepoint_prior_scale, changepoint_range=changepoint_range)
            m.fit(df)
            future = m.make_future_dataframe(periods=period, freq=freq)
            forecast = m.predict(future)
            st.write(forecast)
            fig1 = m.plot(forecast)
            fig2 = m.plot_components(forecast)
            st.write('---')
            st.header('**Forecast**')
            st.pyplot(fig1)
            st.write('---')
            st.header('**Forecast Components**')
            st.write(fig2)
            forecasting_params = {
                'y': y, 
                'ds': ds,
                'df': df,
                'm': m,
                'freq': freq,
                'period': period,
                'seasonality': seasonality,
                'changepoint_prior_scale': changepoint_prior_scale,
                'changepoint_range': changepoint_range
            }
            def forecasting_parameters(forecasting_params):
                for key, value in forecasting_params.items():
                    st.session_state[key] = value
            forecasting_parameters(forecasting_params)

if __name__ == "__main__":
    forecast()