from flask import Flask, request, jsonify
import sqlite3
from flask import *
import uuid

class Student:
    def __init__(self, firstname, lastname, department):
        self.id = uuid.uuid4().hex
        self.firstname = firstname
        self.lastname = lastname
        self.department = department 

app = Flask(__name__)

def connect_db():
    c = sqlite3.connect("student.db").cursor()
    c.execute("CREATE TABLE IF NOT EXISTS STUDENTS("
              "id TEXT, firstname TEXT, lastname TEXT, department TEXT)")
    c.connection.close()

@app.route('/', methods=['GET'])
def index():
    connect_db()
    return render_template('test.html') 

@app.route('/getStudents', methods=['GET'])
def getStudents():
    c = sqlite3.connect('student.db').cursor()
    c.execute("SELECT * FROM STUDENTS")
    data = c.fetchall()
    return data   

@app.route('/addStudents', methods=['POST'])
def addStudents():
    db = sqlite3.connect('student.db')
    c = db.cursor()
    student = Student(request.form['firstname'],
                      request.form['lastname'],
                      request.form['department'])
    c.execute("INSERT INTO STUDENTS VALUES(?, ?, ?, ?)", 
              (student.id, student.firstname, student.lastname, student.department))
    db.commit()
    return render_template('test.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method=='GET':
        return jsonify({"response":"Get Request Called"})
    elif request.method=='POST':
        req_json = request.json
        name = req_json['name']
        return jsonify({"response":"Hi "+ name})

if __name__=='__main__':
    app.run(debug=True)