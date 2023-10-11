import pandas as pd
import matplotlib.pyplot as plt
import warnings;

# from statsmodels.sandbox.regression.sympy_diff import df
from statsmodels.tsa.arima.model import ARIMA;

warnings.filterwarnings("ignore")


def load_data(file_name):
    df = pd.read_excel(file_name, engine='openpyxl')
    df['Time'] = pd.to_datetime(df['Time'], format='%YM%m')
    return df


def visualize_moving_average(df):
    df['MovingAverage'] = df['value'].rolling(window=12).mean()
    plt.figure(figsize=(14, 7))
    plt.plot(df['Time'], df['value'], label='Actual Value')
    plt.plot(df['Time'], df['MovingAverage'], label='12-month Moving Average', color='red')
    plt.title('Moving Average Analysis')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def optimize_and_visualize_arima(train, test, df):
    # Optimize ARIMA
    p_range = range(0, 5)
    d_range = range(0, 3)
    q_range = range(0, 5)
    best_aic = float('inf')
    best_order = None
    for p in p_range:
        for d in d_range:
            for q in q_range:
                try:
                    model = ARIMA(train, order=(p, d, q))
                    model_fit = model.fit()
                    if model_fit.aic < best_aic:
                        best_aic = model_fit.aic
                        best_order = (p, d, q)
                except:
                    continue
    print(f"Best ARIMA Order: {best_order} with AIC: {best_aic}")

    # Visualize ARIMA forecast
    model = ARIMA(train, order=best_order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=len(test))
    plt.figure(figsize=(14, 7))
    plt.plot(df['Time'][:len(train)], train, color='blue', label='Training Data')
    plt.plot(df['Time'][len(train):], test, color='green', label='Test Data')
    forecasted_time = [df['Time'].iloc[-1] + pd.DateOffset(months=i + 1) for i in range(len(forecast))]
    plt.plot(forecasted_time, forecast, color='red', linestyle='--', label='Forecasted Data')
    plt.title('ARIMA Forecast vs Actual Data')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()
    return best_order


def detect_anomalies(ts, window=12, z_threshold=2.5):
    """Detect anomalies using rolling mean and standard deviation."""
    rolling_mean = ts.rolling(window=window).mean()
    rolling_std = ts.rolling(window=window).std()

    # Calculate upper and lower bounds
    upper_bound = rolling_mean + (rolling_std * z_threshold)
    lower_bound = rolling_mean - (rolling_std * z_threshold)

    # Identify anomalies
    anomalies = ((ts > upper_bound) | (ts < lower_bound))

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(ts.index, ts, label='Original Data', color='blue')
    plt.plot(ts.index, upper_bound, 'r--', label='Upper Bound / Lower Bound')
    plt.plot(ts.index, lower_bound, 'r--')

    # Highlighting anomalies
    anomaly_dates = ts.index[anomalies]
    anomaly_values = ts[anomalies]
    plt.scatter(anomaly_dates, anomaly_values, color='red', s=100, label='Anomalies')

    plt.title('Time Series Anomaly Detection')
    plt.xlabel('Time')
    plt.xticks(rotation=45)  # Rotate time labels for better readability
    plt.ylabel('Value')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return anomalies, upper_bound, lower_bound


def predict_job_openings(df, order, n=12):
    model = ARIMA(df['value'], order=order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=n)

    forecast_values = forecast.values
    growth_fall = [forecast_values[i] - (df['value'].iloc[-1] if i == 0 else forecast_values[i - 1]) for i in range(n)]

    # Create dates for the forecasted period. This assumes df['Time'] is in datetime format.
    future_dates = [df['Time'].iloc[-1] + pd.DateOffset(months=i) for i in range(1, n + 1)]

    table = pd.DataFrame({
        'Date': future_dates,
        'Forecasted Job Openings': forecast_values,
        'Growth/Fall': growth_fall
    })

    print(table)
    return table
