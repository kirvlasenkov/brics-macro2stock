import requests
import pandas as pd

def get_gdp_data(country_code, start_year, end_year):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code != 200 or not data or len(data) < 2:
        raise Exception("Ошибка при получении данных из API Всемирного банка.")
    
    gdp_data = data[1]
    df = pd.DataFrame(gdp_data)
    df = df[['date', 'value']]
    df.columns = ['Year', 'GDP']
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

# Список для хранения данных ВВП всех стран
all_gdp_data = []

# Получение данных ВВП для всех стран BRICS
for country, code in brics_countries.items():
    print(f"Получение данных ВВП для {country}")
    gdp_df = get_gdp_data(code, start_year, end_year)
    all_gdp_data.append(gdp_df)

# Объединение всех данных в один DataFrame
combined_gdp_df = pd.concat(all_gdp_data)

# Преобразование таблицы в формат с годами по строкам и странами по столбцам
pivot_table = combined_gdp_df.pivot_table(values='GDP', index='Year', columns='Country')

# Вывод результирующей таблицы
print(pivot_table)
