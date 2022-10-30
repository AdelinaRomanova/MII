from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/analys')
def analys():
    data = request.args
    df = pd.read_csv('market.csv', sep='\t')

    df.rename(
        columns={'Year_Birth': 'День рождения', 'Education': 'Образование', 'Marital_Status': 'Семейное положение',
                 'Income': 'Доход', 'Kidhome': 'Дети', 'Teenhome': 'Подростки', 'Dt_Customer': 'Дата регистрации',
                 'Recency': 'Дни с последней покупки', 'MntWines': 'Вино', 'MntFruits': 'Фрукты',
                 'MntMeatProducts': 'Мясо', "MntFishProducts": 'Рыба', "MntSweetProducts": 'Сладкое',
                 "MntGoldProds": 'Золото', "NumDealsPurchases": 'Покупки со скидкой',
                 "NumWebPurchases": 'Покупки в интернете',
                 "NumCatalogPurchases": 'Покупки по каталогу', "NumStorePurchases": 'Покупки в магазине'}, inplace=True)

    var = df.groupby('Семейное положение').mean()[['Вино']]
    var['Минимальная сумма'] = df.groupby('Семейное положение').min()[['Вино']]
    var['Максимальная сумма'] = df.groupby('Семейное положение').max()[['Вино']]
    var.rename(columns={'Вино': 'Средняя сумма'}, inplace=True)
    prin2 = var.iloc[0:10, 0:10]

    var1 = df.groupby('День рождения').mean()[['Вино']]
    var1['Минимальная сумма'] = df.groupby('День рождения').min()[['Вино']]
    var1['Максимальная сумма'] = df.groupby('День рождения').max()[['Вино']]
    var1.rename(columns={'Вино': 'Средняя сумма'}, inplace=True)
    prin3 = var1.iloc[0:10, 0:10]


    var2 = df.groupby('Образование').mean()[['Вино']]
    var2['Минимальная сумма'] = df.groupby('Образование').min()[['Вино']]
    var2['Максимальная сумма'] = df.groupby('Образование').max()[['Вино']]
    var2.rename(columns={'Зарплата': 'Средняя сумма'}, inplace=True)
    prin4 = var2.iloc[0:10, 0:10]


    var3 = df.groupby('Доход').mean()[['Вино']]
    var3['Минимальная сумма'] = df.groupby('Доход').min()[['Вино']]
    var3['Максимальная сумма'] = df.groupby('Доход').max()[['Вино']]
    var3.rename(columns={'Вино': 'Средняя сумма'}, inplace=True)
    prin5 = var3.iloc[0:10, 0:10]

    description1 = 'Минимальная, максимальная, средняя сумма, сгруппированная по семейному положению'
    description2 = 'Минимальная, максимальная, средняя сумма, сгруппированная по возрасту'
    description3 = 'Минимальная, максимальная, средняя сумма, сгруппированная по образованию'
    description4 = 'Минимальная, максимальная, средняя сумма, сгруппированная по доходу'

    return '<h1 style="text-align: center; padding-top: 15px; font-size: 45px">Набор данных для анализа личночти клиента</h1><br>' \
           + '<h1 style="text-align: center; padding: 0.5%; font-size: 25px">' + description1 + '</h1>' \
           + '<div align="center">' + prin2.to_html() + '</div>' \
           + '<h1 style="text-align: center; padding: 0.5%; font-size: 25px">' + description2 + '</h1>' \
           + '<div align="center">' + prin3.to_html() + '</div>' \
           + '<h1 style="text-align: center; padding: 0.5%; font-size: 25px">' + description3 + '</h1>' \
           + '<div align="center">' + prin4.to_html() + '</div>' \
           + '<h1 style="text-align: center; padding: 0.5%; font-size: 25px">' + description4 + '</h1>' \
           + '<div align="center">' + prin5.to_html() + '</div>' \


if __name__ == '__main__':
    app.run(debug=True)
