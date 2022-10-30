from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/diapason', methods=['GET'])
def table():
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

    # Проверяем диапазон строк
    if int(data['from']) > int(data['to']):
        from_str = int(data['to'])
        to_str = int(data['from'])
    else:
        from_str = int(data['from'])
        to_str = int(data['to'])

    # Проверяем диапазон стобцов
    if int(data['from_st']) > int(data['to_st']):
        from_stl = int(data['to_st'])
        to_stl = int(data['from_st'])
    else:
        from_stl = int(data['from_st'])
        to_stl = int(data['to_st'])

    prim = df.iloc[from_str: to_str, from_stl: to_stl]

    count = df.isna().sum()
    countAll = df.count()

    prim = df.iloc[from_str:to_str, from_stl:to_stl]
    count = df.isna().sum()
    countAll = df.count()

    description_date1 = 'Описание: набор данных предназначен для прогнозирования цены на кофе. ' \
                        'Удобно для регулярного анализа настроений рынка и прогнозирования ценовых изменений в будущем на основе выявленных паттернов.' \
                        'Также это поможет отличить «бычий» рынок (цена закрытия выше, чем цена открытия) от «медвежьего» (цена закрытия ниже, чем цена открытия).'
    description_date2 = 'Описание стоблцов таблицы:'
    description_date3 = str(df.dtypes)

    return render_template("diapason.html", count=count, countAll=countAll, len_str=len(df.axes[0]),
                           len_stl=len(df.axes[1]),
                           description_date1=description_date1,
                           description_date2=description_date2,
                           description_date3=description_date3) \
                            + "<div align='center' >" + prim.to_html() + "</div><br>" \

if __name__ == '__main__':
    app.run(debug=True)
