from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Подключение к базе данных
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='6404',
    database='sm_app'
)
cursor = conn.cursor()

@app.route('/')
def home():
    if 'username' in session:
        return f'Добро пожаловать, {session["username"]}! <a href="/logout">Выйти</a>'
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Неверное имя пользователя или пароль'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
