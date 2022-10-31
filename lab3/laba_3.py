import pandas as pd
from flask import Flask, request
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)

df = pd.read_csv("market.csv", sep='\t')
df2 = pd.read_csv("market.csv", sep='\t')



#дополнение данных приблизительными значениями
for i in range(df.shape[0]-1, round(df.shape[0]*1.1), 1):
    next_id = df['ID'].value_counts().rename_axis('ID').to_frame('counts').index[i % 50]
    next_year = df['Year_Birth'].value_counts().rename_axis('Year_Birth').to_frame('counts').index[i % 50]
    next_education = 'Graduation'
    next_status = 'Single'
    next_income = df['Income'].value_counts().rename_axis('Income').to_frame('counts').index[i % 50]
    next_kidhome = df['Kidhome'].value_counts().rename_axis('Kidhome').to_frame('counts').index[i % 3]
    next_teenhome = df['Teenhome'].value_counts().rename_axis('Teenhome').to_frame('counts').index[i % 3]
    date = datetime.strptime(df['Dt_Customer'].values[i], "%d-%m-%Y")
    next_date = datetime.strftime(date + timedelta(days=1), "%d-%m-%Y")  # следующий день
    next_recency = df['Recency'].value_counts().rename_axis('Recency').to_frame('counts').index[i % 50]
    next_MntWines = df['MntWines'].value_counts().rename_axis('MntWines').to_frame('counts').index[i % 50]
    next_MntFruits = df['MntFruits'].value_counts().rename_axis('MntFruits').to_frame('counts').index[i % 50]
    next_MntMeatProducts = df['MntMeatProducts'].value_counts().rename_axis('MntMeatProducts').to_frame('counts').index[i % 50]
    next_MntFishProducts = df['MntFishProducts'].value_counts().rename_axis('MntFishProducts').to_frame('counts').index[i % 50]
    next_MntSweetProducts = df['MntSweetProducts'].value_counts().rename_axis('MntSweetProducts').to_frame('counts').index[i % 50]
    next_MntGoldProds = df['MntGoldProds'].value_counts().rename_axis('MntGoldProds').to_frame('counts').index[i % 50]
    next_NumDealsPurchases = df['NumDealsPurchases'].value_counts().rename_axis('NumDealsPurchases').to_frame('counts').index[i % 10]
    next_NumWebPurchases = df['NumWebPurchases'].value_counts().rename_axis('NumWebPurchases').to_frame('counts').index[i % 10]
    next_NumCatalogPurchases = df['NumCatalogPurchases'].value_counts().rename_axis('NumCatalogPurchases').to_frame('counts').index[i % 10]
    next_NumStorePurchases = df['NumStorePurchases'].value_counts().rename_axis('NumStorePurchases').to_frame('counts').index[i % 10]
    next_NumWebVisitsMonth = df['NumWebVisitsMonth'].value_counts().rename_axis('NumWebVisitsMonth').to_frame('counts').index[i % 10]
    next_AcceptedCmp3 = df['AcceptedCmp3'].value_counts().rename_axis('AcceptedCmp3').to_frame('counts').index[i % 2]
    next_AcceptedCmp4 = df['AcceptedCmp4'].value_counts().rename_axis('AcceptedCmp4').to_frame('counts').index[i % 2]
    next_AcceptedCmp5 = df['AcceptedCmp5'].value_counts().rename_axis('AcceptedCmp5').to_frame('counts').index[i % 2]
    next_AcceptedCmp1 = df['AcceptedCmp1'].value_counts().rename_axis('AcceptedCmp1').to_frame('counts').index[i % 2]
    next_AcceptedCmp2 = df['AcceptedCmp2'].value_counts().rename_axis('AcceptedCmp2').to_frame('counts').index[i % 2]
    next_Complain = df['Complain'].value_counts().rename_axis('Complain').to_frame('counts').index[i % 2]
    next_Z_CostContact = df['Z_CostContact'].value_counts().rename_axis('Z_CostContact').to_frame('counts').index[i % 1]
    next_Z_Revenue = df['Z_Revenue'].value_counts().rename_axis('Z_Revenue').to_frame('counts').index[i % 1]
    next_Response = df['Response'].value_counts().rename_axis('Response').to_frame('counts').index[i % 2]


    new_row = [next_id, next_year, next_education, next_status, next_income, next_kidhome, next_teenhome,
               next_date, next_recency, next_MntWines, next_MntFruits, next_MntMeatProducts,next_MntFishProducts,
               next_MntSweetProducts, next_MntGoldProds, next_NumDealsPurchases, next_NumWebPurchases, next_NumCatalogPurchases,
               next_NumStorePurchases,next_NumWebVisitsMonth,next_AcceptedCmp3, next_AcceptedCmp4,
               next_AcceptedCmp5, next_AcceptedCmp1,next_AcceptedCmp2, next_Complain, next_Z_CostContact,
               next_Z_Revenue, next_Response]
    df.loc[i+1] = new_row


print(df)
print(df2)
@app.route("/")
def home():
    return "<html>" \
           "<form action='http://127.0.0.1:5000/table' Method=get>" \
           "<h1>Укажите диапазон строк</h1><br>" \
           "<input type=number name=from min=0 value=4>" \
           "<input type=number name=to min=0 value=10>" \
           "<h1>Укажите диапазон столбцов</h1><br>" \
           "<input type=number name=fromst min=0 value=1>" \
           "<input type=number name=tost min=0 value=3><br>" \
           "<br><input type=submit value='Открыть'></form></html>"


@app.route("/table", methods=['GET'])
def table():
    data = request.args

    fig = plt.figure()
    fig.set_size_inches(10, 20)

    df_status = age('Marital_Status', df2)
    df_status_res = pd.DataFrame(df_status, columns=['min', 'max', 'average'])
    df_status_res.plot.bar(rot=0)
    plt.title('Цена на вино в разрезе семейного положения, старый набор данных')

    df_status = age('Marital_Status', df)
    df_status_res = pd.DataFrame(df_status, columns=['min', 'max', 'average'])
    df_status_res.plot.bar(rot=0)
    plt.title('Цена на вино в разрезе семейного положения, новый набор данных')

    df_birth = age('Year_Birth', df2)
    df_birth_res = pd.DataFrame(df_birth, columns=['min', 'max', 'average'])
    df_birth_res.plot.line(rot=0)
    plt.title('Цена на вино в разрезе возраста, старый набор данных')

    df_birth = age('Year_Birth', df)
    df_birth_res = pd.DataFrame(df_birth, columns=['min', 'max', 'average'])
    df_birth_res.plot.line(rot=0)
    plt.title('Цена на вино в разрезе возрвста, новый набор данных')

    df_education_level = age('Education', df2)
    df_education_level_res = pd.DataFrame(df_education_level, columns=['min', 'max', 'average'])
    df_education_level_res.plot.bar(rot=0)
    plt.title('Цена на вино в разрезе обучения, старый набор данных')

    df_education_level = age('Education', df)
    df_education_level_res = pd.DataFrame(df_education_level, columns=['min', 'max', 'average'])
    df_education_level_res.plot.bar(rot=0)
    plt.title('Цена на вино в разрезе обучения, новый набор данных')

    df_income = age('Income', df2)
    df_income_res = pd.DataFrame(df_income, columns=['min', 'max', 'average'])
    df_income_res.plot.line(rot=0)
    plt.title('Цена на вино в разрезе дохода, старый набор данных')

    df_income = age('Income', df)
    df_income_res = pd.DataFrame(df_income, columns=['min', 'max', 'average'])
    df_income_res.plot.line(rot=0)
    plt.title('Цена на вино в разрезе дохода, новый набор данных')

    fig_list = []
    for i in plt.get_fignums():
        tmpfile = io.BytesIO()
        plt.figure(i).savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        fig_list.append('<img src=\'data:image/png;base64,{}\'>'.format(encoded))

    return '<h1 align="center">Набор данных для анализа личночти клиента</h1><br>' \
           + '<br><h2 align="center">Анализ данных</h2>' \
             '<h3 align="center">Минимальная, максимальная, средняя цена на вино в разрезе семейного положения (старые данные)</h3>' \
           + '<div align="center">' + filt('Marital_Status', df2) + '</div>' \
           + '<h3 align="center">Минимальная, максимальная, средняя цена на вино в разрезе семейного положения (новые данные)</h3>' \
           + '<div align="center">' + filt('Marital_Status', df) + '</div>' \
           + '<br align="center"><h3 align="center">Минимальная, максимальная, средняя цена на вино в разрезе возраста (старые данные)</h3>' \
           + '<div align="center">' + filt('Year_Birth', df2) + '</div>' \
           + '<br align="center"><h3 align="center">Минимальная, максимальная, средняя цена на вино в разрезе возраста (новые данные)</h3>' \
           + '<div align="center">' + filt('Year_Birth', df) + '</div>' \
           + '<br align="center"><h3 align="center">Минимальная, максимальная, средняя цена на вино в разрезе уровня обучения (старые данные)</h3>' \
           + '<div align="center">' + filt('Education', df2) + '</div>' \
           + '<br align="center"><h3 align="center">Минимальная, максимальная, средняя цена на вино в разрезе уровня обучения (новые данные)</h3>' \
           + '<div align="center">' + filt('Education', df) + '</div>' \
           + '<br><h3 align="center">Минимальная, максимальная, средняя цена на вино в разрезе дохода (старые данные)</h3>' \
           + '<div align="center">' + filt('Income', df2) + '</div>' \
           + '<br><h3 align="center">Минимальная, максимальная, средняя цена на вино в разрезе дохода (новые данные)</h3>' \
           + '<div align="center">' + filt('Income', df) + '</div>' \
           + '<br><h2 align="center">Визуализация данных</h2>' \
           + '<div align="center">' + fig_list[1] + fig_list[2] + fig_list[3] + fig_list[4] + fig_list[5] + fig_list[6] + fig_list[7] + fig_list[8] + '<div>'

def age(group_column, df):
    age = df.groupby(group_column).min()[['MntWines']]
    age.rename(columns={'MntWines': 'min'}, inplace=True)
    max_age = df.groupby(group_column).max()[['MntWines']]
    mean_age = df.groupby(group_column).mean()[['MntWines']]
    age['max'] = max_age['MntWines']
    age['average'] = mean_age['MntWines']
    return age

def filt(group_column, df2):
    age = df2.groupby(group_column).min()[['MntWines']]
    age.rename(columns={'MntWines': 'Min MntWines'}, inplace=True)
    max_age = df2.groupby(group_column).max()[['MntWines']]
    mean_age = df2.groupby(group_column).mean()[['MntWines']].round(decimals=2)
    age['Max MntWines'] = max_age['MntWines']
    age['Average MntWines'] = mean_age['MntWines']
    return age.to_html()

if __name__ == "__main__":
    app.run(debug=True)