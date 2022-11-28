from flask import Flask, request, render_template
from sklearn import tree
import pandas as pd
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask('__name__')

df = pd.read_csv("market.csv", sep='\t')

#начальная страница
@app.route('/')
def home():
    # return render_template("home.html", about=about)
    return render_template("home.html")

@app.route('/tree_market')
def tree_market():
    X = df.drop(columns=['ID', 'Marital_Status', 'Income', 'Kidhome', 'Teenhome', 'Dt_Customer',
                         'Recency', 'Education', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
                         'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases', 'NumWebPurchases',
                         'NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth', 'AcceptedCmp3',
                         'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2', 'Complain', 'Z_CostContact',
                         'Z_Revenue', 'Response']).iloc[:25]
    Y = df['Education'].iloc[:25]
    model = tree.DecisionTreeClassifier(criterion="entropy")
    model.fit(X, Y)
    plt.figure(figsize=(20, 20))

    class_names = ['Graduation', 'PhD', 'Master', 'Basic', '2n Cycle']

    tree.plot_tree(model, class_names=class_names)

    tmpfile = BytesIO()  # создание временного файла
    plt.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')  # кодирование

    return render_template("tree.html", encoded=encoded, score=model.score(X,Y).round(2))

@app.route('/model_evaluation')
def model_evaluation():
    X = df.drop(columns=['ID', 'Marital_Status', 'Income', 'Kidhome', 'Teenhome', 'Dt_Customer',
                         'Recency', 'Education', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
                         'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases', 'NumWebPurchases',
                         'NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth', 'AcceptedCmp3',
                         'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2', 'Complain', 'Z_CostContact',
                         'Z_Revenue', 'Response']).iloc[:25]
    Y = df['Education'].iloc[:25]
    model = tree.DecisionTreeClassifier(criterion="entropy")
    model.fit(X, Y)

    XY_real = df.drop(['ID', 'Marital_Status', 'Income', 'Kidhome', 'Teenhome', 'Dt_Customer',
                         'Recency', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
                         'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases', 'NumWebPurchases',
                         'NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth', 'AcceptedCmp3',
                         'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2', 'Complain', 'Z_CostContact',
                         'Z_Revenue', 'Response'], axis=1).iloc[25:30]
    XY_train = XY_real.copy()
    XY_train['Education'] = XY_train.apply(lambda x: model.predict([[int(x['Year_Birth']), float(x['MntWines'])]]),  axis=1)

    return render_template("model_evaluation.html", result=8.2) \
           + '<br>Реальные данные' + XY_real.to_html() + '<br>Сгенерированные данные' + XY_train.to_html()



# запуск HTTP-сервера
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
