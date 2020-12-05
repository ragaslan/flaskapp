from flask import Flask,render_template,request,logging,redirect,url_for,session
from flask_mysqldb import MySQL
from functools import wraps


app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "us"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
app.secret_key = "super secret key"

mysql = MySQL(app)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['logged_in'] == True:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return decorated_function



@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        cursor = mysql.connection.cursor()
        sorgu = "select * from uyeler where user_name = %s"
        result = cursor.execute(sorgu,(username,))
        if result > 0 :
            data = cursor.fetchone()
            realpass = data['user_password']
            if realpass == password:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('profile'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run()
