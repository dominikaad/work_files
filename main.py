import sqlite3

from flask import Flask, render_template, request, flash
con = sqlite3.connect('bd1.db', check_same_thread=False)
cursor = con.cursor()
app = Flask(__name__)

@app.route('/')
def page_index():
    cursor.execute("SELECT * FROM inform")
    a = cursor.fetchall()
    return render_template('first.html', a=a)

@app.route('/add_post/')
def add_post():
    return render_template('add.html')

@app.route('/upload/', methods=['POST'])
def save_post():
    image = request.files.getlist('image')
    for i in image:
        title = request.form['title']
        description = request.form['description']
        a = f'static/uploads/{i.filename}'
        i.save(a)
        cursor.execute(
            "INSERT INTO inform (title, file_name, description) VALUES (?,?,?)",
            [title, a, description])
        con.commit()
    return 'Your file is saved'

@app.route('/detail/<i>')
def post(i):
    cursor.execute('SELECT * FROM inform WHERE id = (?)', [i])
    b = cursor.fetchall()
    return render_template('detail.html', b=b)

app.run(debug=True)