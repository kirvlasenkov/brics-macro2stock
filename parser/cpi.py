import requests
import pandas as pd

def get_cpi_data(country_code, start_year, end_year):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/FP.CPI.TOTL?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code != 200 or not data or len(data) < 2:
        raise Exception("Ошибка при получении данных из API Всемирного банка.")
    
    cpi_data = data[1]
    df = pd.DataFrame(cpi_data)
    df = df[['date', 'value']]
    df.columns = ['Year', 'CPI']
    df['Country'] = country_code
    
    return df

# Список кодов стран BRICS
brics_countries = {
    'Brazil': 'BRA',
    'Russia': 'RUS',
    'India': 'IND',
    'China': 'CHN',
    'South Africa': 'ZAF'
}

# Период для получения данных
start_year = 1990
end_year = 2022

# Список для хранения данных CPI всех стран
all_cpi_data = []

# Получение данных CPI для всех стран BRICS
for country, code in brics_countries.items():
    print(f"Получение данных CPI для {country}")
    cpi_df = get_cpi_data(code, start_year, end_year)
    all_cpi_data.append(cpi_df)

# Объединение всех данных в один DataFrame
combined_cpi_df = pd.concat(all_cpi_data)

# Преобразование таблицы в формат с годами по строкам и странами по столбцам
pivot_table_cpi = combined_cpi_df.pivot_table(values='CPI', index='Year', columns='Country')

# Вывод результирующей таблицы
print(pivot_table_cpi)
