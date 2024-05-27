import requests
import pandas as pd

def get_exchange_rate_data(country_code, start_year, end_year):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/PA.NUS.FCRF?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Ошибка при выполнении запроса к API Всемирного банка для {country_code}. Код ошибки: {response.status_code}")
    
    data = response.json()
    if not data or len(data) < 2:
        raise Exception(f"Ошибка при получении данных из API Всемирного банка для {country_code}. Данные отсутствуют или некорректны.")
    
    exchange_rate_data = data[1]
    df = pd.DataFrame(exchange_rate_data)
    df = df[['date', 'value']]
    df.columns = ['Year', 'ExchangeRate']
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
start_year = 2010
end_year = 2020

# Список для хранения данных валютных курсов всех стран
all_exchange_rate_data = []

# Получение данных валютных курсов для всех стран BRICS
for country, code in brics_countries.items():
    try:
        print(f"Получение данных валютных курсов для {country}")
        exchange_rate_df = get_exchange_rate_data(code, start_year, end_year)
        all_exchange_rate_data.append(exchange_rate_df)
    except Exception as e:
        print(e)

# Объединение всех данных в один DataFrame
if all_exchange_rate_data:
    combined_exchange_rate_df = pd.concat(all_exchange_rate_data)
    # Преобразование таблицы в формат с годами по строкам и странами по столбцам
    pivot_table_exchange_rate = combined_exchange_rate_df.pivot_table(values='ExchangeRate', index='Year', columns='Country')
    # Вывод результирующей таблицы
    print(pivot_table_exchange_rate)
else:
    print("Нет данных для создания таблицы.")
