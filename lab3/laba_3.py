from flask import Flask, request, render_template
import pandas as pd
from bitarray import bitarray
import math

app = Flask(__name__)

df = pd.read_csv("market.csv", sep='\t')
kaggleArr = ["my",
             "https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database",
             "https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries",
             "https://www.kaggle.com/datasets/surajjha101/stores-area-and-sales-data",
             "https://www.kaggle.com/datasets/spscientist/students-performance-in-exams",
             "https://www.kaggle.com/datasets/ankanhore545/100-highest-valued-unicorns",
             "https://www.kaggle.com/datasets/sadeghjalalian/ufo-sightings-in-usa",
             "https://www.kaggle.com/datasets/shariful07/student-flexibility-in-online-learning",
             "https://www.kaggle.com/datasets/rashikrahmanpritom/heart-attack-analysis-prediction-dataset",
             "https://www.kaggle.com/datasets/surajjha101/forbes-billionaires-data-preprocessed",
             "https://www.kaggle.com/datasets/midhundasl/mobile-price-hike-data",
             ]
ArrKeyWord = ["income", "education", "kidhome",
              "health", "diabetes", "India",
              "salary", "salary_in_usd", "remote_ratio",
              "supermarket", "store", "sales",
              "education", "exam", "student",
              "state", "city", "industries",
              "shape", "duration", "stats",
              "gender", "device", "location"
              "age", "sex", "cp",
              "name", "networth", "industry",
              "model", "processor", "base_color",
              ]


@app.route('/')
def home():
    return "<html><form action='http://127.0.0.1:5000/filter' method=get><h2>Введите слово для поиска:" \
           "</h2><input type=text size=18 " \
           "name=keyWord><br><input type=submit value='Найти'></form></html>"

class Filter(object):
    def __init__(self, size, number_expected_elements=100):
        self.size = size
        self.number_expected_elements = number_expected_elements
        self.filter = bitarray(self.size)
        self.filter.setall(0)
        self.number_hash_functions = round((self.size / self.number_expected_elements) * math.log(2))

    def _hash_djb2(self, s):
        hash = 5381
        for x in s:
            hash = ((hash << 5) + hash) + ord(x)
        return hash % self.size

    def _hash(self, item, K):
        return self._hash_djb2(str(K) + item)

    def add_to_filter(self, item):
        for i in range(self.number_hash_functions):
            self.filter[self._hash(item, i)] = 1

    def check_is_not_in_filter(self, item):
        for i in range(self.number_hash_functions):
            if self.filter[self._hash(item, i)] == 0:
                return True
        return False

@app.route('/filter', methods=['GET'])
def filter():
    data = request.args
    bloom_filter = Filter(200, 100)

    for i in range(len(ArrKeyWord)):
        bloom_filter.add_to_filter(ArrKeyWord[i])

    if not bloom_filter.check_is_not_in_filter(data['keyWord']):
        for i in range(len(ArrKeyWord)):
            if ArrKeyWord[i] == data['keyWord']:
                place = i
                break

        if place // 3 == 0:
            newdf = df.iloc[0: 20, 0: 8]
            return '<h1>Результаты поиска: Набор данных об анализе личности клиента</h1><br>' \
                   + '<div>' + newdf.to_html() + '</div>' + '<form action=\'http://127.0.0.1:5000/\' method=get><input type=submit value=\'Возврат к фильтру\'></form>'

        else:
            return '<h1>Результаты поиска: Набор данных c источника Kaggle: </h1><br>' \
                   + '<div><a href="' + kaggleArr[place // 3] + '" target="_blank">Перейти к источнику</a></div>' + '<form action=\'http://127.0.0.1:5000/\' method=get><input type=submit value=\'Возврат к фильтру\'></form>'

    else:
        return "<html><form action='http://127.0.0.1:5000/' method=get><h2>Данные не найдены" \
               "</h2><br><input type=submit value='Возврат к фильтру'></form></html>"
if __name__ == '__main__':
    app.run(debug=True)






