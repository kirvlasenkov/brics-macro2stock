import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# Функция для построения модели ARMA и прогнозирования
def build_and_forecast_arma(data, country, column, order=(2, 0)):
    # Выбор временного ряда для анализа
    ts = data[column].dropna()  # Удаление пропущенных значений
    
    # Проверка на стационарность временного ряда
    result = sm.tsa.adfuller(ts)
    print(f"ADF Statistic for {column}: {result[0]}")
    print(f"p-value for {column}: {result[1]}")
    for key, value in result[4].items():
        print('Critical Values:')
        print(f"   {key}: {value}")
    
    # Построение модели ARMA (используя ARIMA с d=0)
    model = ARIMA(ts, order=(order[0], 0, order[1])).fit()
    
    # Прогнозирование на 10 периодов вперед
    forecast_steps = 40
    forecast = model.get_forecast(steps=forecast_steps)
    forecast_df = forecast.summary_frame()['mean']
    forecast_index = pd.date_range(start=ts.index[-1], periods=forecast_steps+1, freq='Y')[1:]
    forecast_df.index = forecast_index
    
    # Визуализация результатов
    plt.figure(figsize=(12, 6))
    plt.plot(ts, label=f'Historical {column}')
    plt.plot(forecast_df, label=f'Forecast {column}', color='red')
    plt.xlabel('Year')
    plt.ylabel(column)
    plt.title(f'{country} - {column} ARMA Model Forecast')
    plt.legend()
    plt.show()
    
    # График остатков
    residuals = model.resid
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.histplot(residuals, kde=True, color='blue')
    plt.title(f'{country} - {column} Residuals Histogram')
    plt.subplot(1, 2, 2)
    sm.qqplot(residuals, line='s', ax=plt.gca())
    plt.title(f'{country} - {column} QQ Plot')
    plt.tight_layout()
    plt.show()
    
    # Автокорреляция остатков
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sm.graphics.tsa.plot_acf(residuals, lags=20, ax=plt.gca())
    plt.title(f'{country} - {column} ACF of Residuals')
    plt.subplot(1, 2, 2)
    sm.graphics.tsa.plot_pacf(residuals, lags=20, ax=plt.gca())
    plt.title(f'{country} - {column} PACF of Residuals')
    plt.tight_layout()
    plt.show()
    
    return model, forecast_df

# Пример для Бразилии
country = 'Russia'
data = pd.read_csv(f'{country}_macro_stock_data.csv', index_col='Year')
data.index = pd.to_datetime(data.index, format='%Y')

# Параметры модели ARMA (p, q)
arma_order = (2, 2)



# Построение и прогнозирование модели ARMA для StockIndex
arma_model_stock, forecast_stock = build_and_forecast_arma(data, country, 'StockIndex', order=arma_order)
