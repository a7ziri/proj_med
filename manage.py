import flask
import mysql.connector
from flask import Flask, render_template, request, redirect, session, url_for




con = mysql.connector.connect(
    #user='rnovikov',
    user='root',
    password='Dend1y13',
    #password='Qwerty123',
    #host='ubuntu2',
    host='localhost',
    database='doctor'
    #database='fistech'
)
print('connect')
cur = con.cursor()



def create_table():

    create= """
    CREATE TABLE IF NOT EXISTS syptom_name(
        id_records INT AUTO_INCREMENT PRIMARY KEY,
        symptom CHAR(100),
        symptom_number INT
    )
    """
    cur.execute(create)


app = Flask(__name__)

@app.route('/main')
def mainpage():
    return render_template("mainpage.html", methods=['POST','GET'])


@app.route('/main/doctoranalyzer', methods=['POST','GET'])
def analyse():
    if flask.request.method == 'POST':
        field_list = []
        for key, val in request.form.items():
            if key.startswith("field"):
                field_list.append(val)
                print(field_list)
        
        #syptom_list = field_list


    return render_template("index.html", methods=['POST','GET']) #syptom_list=syptom_list)





if __name__ == '__main__':
    #create_table()
    app.run(host="localhost", port=9999, debug=True)