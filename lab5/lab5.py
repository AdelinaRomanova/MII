from flask import Flask
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

df = pd.read_csv("market.csv", sep='\t')

class LinearRegression:
    def __init__(self, df, fig, axes):
        self.df = df
        self.fig = fig
        self.axes = axes

    def manual(self):
        def linear_regression(x_val):
            return a + b * x_val

        # 99%
        k = round(len(self.df.axes[0]) * 0.99)
        x = self.df["MntWines"][:k]
        y = self.df["Income"][:k]
        sum_x = x.sum()
        sum_y = y.sum()
        sum_xy = 0
        n = x.size
        for i in range(0, n):
            if y._get_value(i) is float or y._get_value(i) is int:
                sum_xy += x._get_value(i) * y._get_value(i)
            else:
                sum_xy += x._get_value(i) * 20000
        sum_x2 = 0
        for i in range(0, n):
            sum_x2 += x._get_value(i) ** 2

        b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - (sum_x ** 2))
        a = (sum_y - b * sum_x) / n

        x_plot = list()
        y_plot = list()

        for i in range(int(x.min()), int(x.max())):
            x_plot.append(i)
            y_plot.append(linear_regression(i))

        self.axes[0].scatter(x, y)
        self.axes[0].set_title('99% ручной')
        self.axes[0].set_xlabel('Затраты на вино')
        self.axes[0].set_ylabel('Доход')
        self.axes[0].plot(x_plot, y_plot, "r")

        # 1%
        k = round(len(self.df.axes[0]) * 0.01)
        x = self.df["MntWines"][-k:]
        y = self.df["Income"][-k:]
        sum_x = x.sum()
        sum_y = y.sum()
        sum_xy = 0
        n = x.size
        for i in range(0, n):
            if y._get_value(i,1) is float or y._get_value(i,1) is int:
                sum_xy += x._get_value(i, 1) * y._get_value(i, 1)
            else:
                sum_xy += x._get_value(i, 1) * 20000
        sum_x2 = 0
        for i in range(0, n):
            sum_x2 += x._get_value(i, 1) ** 2

        b = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - (sum_x ** 2))
        a = (sum_y - b * sum_x) / n

        x_plot = list()
        y_plot = list()

        for i in range(int(x.min()), int(x.max())):
            x_plot.append(i)
            y_plot.append(linear_regression(i))

        self.axes[1].scatter(x, y)
        self.axes[1].set_title('1% ручной')
        self.axes[1].set_xlabel('Затраты на вино')
        self.axes[1].set_ylabel('Доход')
        self.axes[1].plot(x_plot, y_plot, "r")

@app.route('/')
def home():
    return "<html>" \
            "<form Action='http://127.0.0.1:5000/linear' Method='get'>" \
           "<input type=submit value='Линейная регрессия'></form>" \
           "</html>"

@app.route('/linear', methods=['GET'])
def linear():
    fig, axes = plt.subplots(1, 2)
    linear_regression = LinearRegression(df, fig, axes)
    linear_regression.manual()
    fig.set_figwidth(20)
    plt.savefig("static/linear_plts.png")
    return "<h1 align=center>Зависимость трат на вино от дохода семьи клиента</h1><br>" \
           + '<img width="90%" src="/static/linear_plts.png"/>'

if __name__ == '__main__':
    app.run(debug=True)






