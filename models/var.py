import pandas as pd
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt

# Функция для построения и анализа модели VAR
def build_and_analyze_var(data, country):
    # Выбор временных рядов для анализа (все макроэкономические показатели и фондовый индекс)
    variables = data[['GDP', 'CPI', 'Unemployment', 'M2', 'InterestRate', 'ExchangeRate', 'TradeBalance', 'GovernmentDebt', 'StockIndex']]
    
    # Построение модели VAR
    model = VAR(variables)
    results = model.fit(maxlags=2)
    
    # Вывод результатов модели
    print(results.summary())
    
    # Прогнозирование на 10 лет вперед
    forecast_steps = 30
    forecast = results.forecast(variables.values[-results.k_ar:], steps=forecast_steps)
    forecast_index = pd.date_range(start=variables.index[-1], periods=forecast_steps+1, freq='Y')[1:]
    forecast_df = pd.DataFrame(forecast, index=forecast_index, columns=variables.columns)
    
    # Визуализация прогнозов для StockIndex
    plt.figure(figsize=(12, 6))
    plt.plot(variables.index, variables['StockIndex'], label='Historical StockIndex')
    plt.plot(forecast_df.index, forecast_df['StockIndex'], label='Forecast StockIndex', color='red')
    plt.xlabel('Year')
    plt.ylabel('StockIndex')
    plt.title(f'{country} - VAR Model Forecast for StockIndex')
    plt.legend()
    plt.show()
    
    # Анализ импульсных откликов
    irf = results.irf(10)
    irf.plot(orth=False)
    plt.suptitle(f'{country} - Impulse Response Functions')
    plt.show()
    
    # Декомпозиция дисперсии
    fevd = results.fevd(10)
    fevd.plot()
    plt.suptitle(f'{country} - Forecast Error Variance Decomposition')
    plt.show()
    
    return results, forecast_df

# Пример для Бразилии
country = 'India'
data = pd.read_csv(f'{country}_macro_stock_data.csv', index_col='Year')
data.index = pd.to_datetime(data.index, format='%Y')

# Построение и анализ модели VAR для Бразилии
var_results, forecast_df = build_and_analyze_var(data, country)
