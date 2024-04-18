from flask import Flask, render_template, request
from sklearn.tree import DecisionTreeClassifier
import pickle
import psycopg2

def postgresql_connent():
    conn = psycopg2.connect(database="postgres",
                            host="127.0.0.1",
                            user="postgres",
                            password="123456",
                            port="5432")
    return conn

dct = pickle.load(open('dct.pkl', 'rb'))

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        sepal_length = float(request.form.get('sepal_length'))
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])
        iris_array = [[sepal_length, sepal_width, petal_length,petal_width]]
        prediction = dct.predict(iris_array)
        conn = postgresql_connent()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO local(sepal_length, sepal_width, petal_length, petal_width, prediction) VALUES ({sepal_length}, {sepal_width}, {petal_length}, {petal_width}, '{prediction[0]}');")
        conn.commit()
        conn.close()
        return render_template("index.html", prediction = prediction[0].capitalize())
    else:
        return render_template("index.html")

@app.route('/All_result')
def all_result():
    conn = postgresql_connent()
    cur = conn.cursor()
    cur.execute("SELECT * FROM local")
    data = cur.fetchall()
    conn.close()
    return render_template("all_result.html", data=data)



if __name__ == '__main__':
    app.run()
    