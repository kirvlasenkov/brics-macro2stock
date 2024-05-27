import pandas as pd
import numpy as np
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Функция для предварительной обработки данных
def preprocess_data(data):
    # Заполнение пропущенных значений ближайшими вперед и назад
    data = data.ffill().bfill()
    
    # Нормализация данных (исключая столбцы 'Year' и 'StockIndex')
    features = data.columns.difference(['Year', 'StockIndex'])
    scaler = StandardScaler()
    data[features] = scaler.fit_transform(data[features])
    
    return data

# Функция для выполнения регрессионного анализа
def perform_regression_analysis(data, country):
    X = data.drop(columns=['Year', 'StockIndex'])
    y = data['StockIndex']
    
    # Добавление константы (Intercept) в модель
    X = sm.add_constant(X)
    
    # Проверка на наличие NaN или бесконечных значений после обработки
    if not np.isfinite(X).all().all() or not np.isfinite(y).all():
        raise ValueError("Данные содержат NaN или бесконечные значения после обработки.")
    
    # Построение модели
    model = sm.OLS(y, X).fit()
    
    # Вывод результатов
    print(f"Регрессионный анализ для {country}")
    print(model.summary())
    
    # Уравнение регрессии
    equation = "StockIndex = "
    for i, coef in enumerate(model.params):
        if i == 0:
            equation += f"{coef:.2f} + "
        else:
            equation += f"{coef:.2f} * {X.columns[i]} + "
    equation = equation.rstrip(" + ")
    print(f"Уравнение регрессии для {country}: {equation}\n")
    
    return model

# Функция для построения графиков
def plot_regression_results(model, data, country):
    # Построение графика остатков
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.residplot(x=model.fittedvalues, y=model.resid, lowess=True, line_kws={'color': 'red'})
    plt.xlabel('Fitted values')
    plt.ylabel('Residuals')
    plt.title(f'{country} - Residuals vs Fitted values')

    # Построение графика QQ
    plt.subplot(1, 2, 2)
    sm.qqplot(model.resid, line='s', ax=plt.gca())
    plt.title(f'{country} - QQ plot')

    plt.tight_layout()
    plt.show()

# Список стран BRICS
brics_countries = ['Brazil', 'Russia', 'India', 'China', 'South Africa']

# Проведение регрессионного анализа для каждой страны
for country in brics_countries:
    # Загрузка данных для страны
    try:
        data = pd.read_csv(f'{country}_macro_stock_data.csv')
    except FileNotFoundError:
        print(f"Data for {country} not found. Skipping.")
        continue
    
    # Предварительная обработка данных
    data = preprocess_data(data)
    
    # Проверка, есть ли данные после обработки
    if data.empty:
        print(f"Нет данных для анализа для {country}")
        continue
    
    # Выполнение регрессионного анализа
    try:
        model = perform_regression_analysis(data, country)
        
        # Построение графиков для регрессии
        plot_regression_results(model, data, country)
        
        # Проверка статистической значимости регрессоров
        significant_vars = model.pvalues[model.pvalues < 0.05].index.tolist()
        print(f"Статистически значимые переменные для {country}: {significant_vars}")
        
    except ValueError as e:
        print(f"Ошибка при анализе данных для {country}: {e}")
