import yfinance as yf
import pandas as pd

# Список фондовых индексов для стран BRICS
brics_indices = {
    'Brazil': '^BVSP',
    'Russia': 'IMOEX.ME',
    'India': '^BSESN',
    'China': '000001.SS',
    'South Africa': '^JALSH'
}

# Период для получения данных
start_date = '1990-01-01'
end_date = '2022-12-31'

# Список для хранения данных фондовых индексов всех стран
all_stock_index_data = []

# Получение данных фондовых индексов для всех стран BRICS
for country, index in brics_indices.items():
    print(f"Получение данных фондового индекса для {country}")
    stock_data = yf.download(index, start=start_date, end=end_date, progress=False)
    stock_data.reset_index(inplace=True)
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    stock_data['Year'] = stock_data['Date'].dt.year
    yearly_stock_data = stock_data.groupby('Year')['Close'].mean().reset_index()
    yearly_stock_data.columns = ['Year', 'StockIndex']
    yearly_stock_data['Country'] = country
    all_stock_index_data.append(yearly_stock_data)

# Объединение всех данных в один DataFrame
combined_stock_index_df = pd.concat(all_stock_index_data)

# Преобразование таблицы в формат с годами по строкам и странами по столбцам
pivot_table_stock_index = combined_stock_index_df.pivot_table(values='StockIndex', index='Year', columns='Country')

# Вывод результирующей таблицы
print(pivot_table_stock_index)

