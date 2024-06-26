import requests
import pandas as pd

def get_unemployment_data(country_code, start_year, end_year):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/SL.UEM.TOTL.ZS?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Ошибка при выполнении запроса к API Всемирного банка для {country_code}. Код ошибки: {response.status_code}")
    
    data = response.json()
    if not data or len(data) < 2:
        raise Exception(f"Ошибка при получении данных из API Всемирного банка для {country_code}. Данные отсутствуют или некорректны.")
    
    unemployment_data = data[1]
    df = pd.DataFrame(unemployment_data)
    df = df[['date', 'value']]
    df.columns = ['Year', 'Unemployment']
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

# Список для хранения данных уровня безработицы всех стран
all_unemployment_data = []

# Получение данных уровня безработицы для всех стран BRICS
for country, code in brics_countries.items():
    try:
        print(f"Получение данных уровня безработицы для {country}")
        unemployment_df = get_unemployment_data(code, start_year, end_year)
        all_unemployment_data.append(unemployment_df)
    except Exception as e:
        print(e)

# Объединение всех данных в один DataFrame
if all_unemployment_data:
    combined_unemployment_df = pd.concat(all_unemployment_data)
    # Преобразование таблицы в формат с годами по строкам и странами по столбцам
    pivot_table_unemployment = combined_unemployment_df.pivot_table(values='Unemployment', index='Year', columns='Country')
    # Вывод результирующей таблицы
    print(pivot_table_unemployment)
else:
    print("Нет данных для создания таблицы.")
