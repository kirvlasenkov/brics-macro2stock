import requests
import pandas as pd

def get_m2_data(country_code, start_year, end_year):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/FM.LBL.BMNY.GD.ZS?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Ошибка при выполнении запроса к API Всемирного банка для {country_code}. Код ошибки: {response.status_code}")
    
    data = response.json()
    if not data or len(data) < 2:
        raise Exception(f"Ошибка при получении данных из API Всемирного банка для {country_code}. Данные отсутствуют или некорректны.")
    
    m2_data = data[1]
    df = pd.DataFrame(m2_data)
    df = df[['date', 'value']]
    df.columns = ['Year', 'M2']
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

# Список для хранения данных M2 всех стран
all_m2_data = []

# Получение данных M2 для всех стран BRICS
for country, code in brics_countries.items():
    try:
        print(f"Получение данных M2 для {country}")
        m2_df = get_m2_data(code, start_year, end_year)
        all_m2_data.append(m2_df)
    except Exception as e:
        print(e)

# Объединение всех данных в один DataFrame
if all_m2_data:
    combined_m2_df = pd.concat(all_m2_data)
    # Преобразование таблицы в формат с годами по строкам и странами по столбцам
    pivot_table_m2 = combined_m2_df.pivot_table(values='M2', index='Year', columns='Country')
    # Вывод результирующей таблицы
    print(pivot_table_m2)
else:
    print("Нет данных для создания таблицы.")
