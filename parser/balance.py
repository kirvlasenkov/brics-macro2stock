import requests
import pandas as pd

def get_trade_balance_data(country_code, start_year, end_year):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/NE.RSB.GNFS.CD?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Ошибка при выполнении запроса к API Всемирного банка для {country_code}. Код ошибки: {response.status_code}")
    
    data = response.json()
    if not data or len(data) < 2:
        raise Exception(f"Ошибка при получении данных из API Всемирного банка для {country_code}. Данные отсутствуют или некорректны.")
    
    trade_balance_data = data[1]
    df = pd.DataFrame(trade_balance_data)
    df = df[['date', 'value']]
    df.columns = ['Year', 'TradeBalance']
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

# Список для хранения данных торгового баланса всех стран
all_trade_balance_data = []

# Получение данных торгового баланса для всех стран BRICS
for country, code in brics_countries.items():
    try:
        print(f"Получение данных торгового баланса для {country}")
        trade_balance_df = get_trade_balance_data(code, start_year, end_year)
        all_trade_balance_data.append(trade_balance_df)
    except Exception as e:
        print(e)

# Объединение всех данных в один DataFrame
if all_trade_balance_data:
    combined_trade_balance_df = pd.concat(all_trade_balance_data)
    # Преобразование таблицы в формат с годами по строкам и странами по столбцам
    pivot_table_trade_balance = combined_trade_balance_df.pivot_table(values='TradeBalance', index='Year', columns='Country')
    # Вывод результирующей таблицы
    print(pivot_table_trade_balance)
else:
    print("Нет данных для создания таблицы.")
