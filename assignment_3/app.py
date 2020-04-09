from flask import Flask, render_template, url_for, redirect, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
DATABASE = './login.db'
#The stuff below is from the Week 13 tutorial
# connects to the database
def get_db():
    # if there is a database, use it
    db = getattr(g, '_login', None)
    if db is None:
        # otherwise, create a database to use
        db = g._login = sqlite3.connect(DATABASE)
    return db

# converts the tuples from get_db() into dictionaries
# (don't worry if you don't understand this code)
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# given a SELECT query, executes and returns the result
# (don't worry if you don't understand this code)
def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

app = Flask(__name__)

# this function gets called when the Flask app shuts down
# tears down the database connection
@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
        # close the database if we are connected to it
		db.close()

#It makes the database login.db and initiates the login manager. Source: https://www.youtube.com/watch?v=8aTnmsDMldY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

#User class, it's what we send and get from the database. Source: https://www.youtube.com/watch?v=8aTnmsDMldY
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))
	
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
	
@app.route('/')
@app.route('/index')
def home():
	return render_template('index.html')


@app.route('/assignments')
def assignments():
	return render_template('assignments.html')


@app.route('/calendar')
def calendar():
	return render_template('calendar.html')


@app.route('/course_team')
def course_team():
	return render_template('course_team.html')


@app.route('/feedback')
def feedback():
	return render_template('feedback.html')


@app.route('/labs')
def labs():
	return render_template('labs.html')


@app.route('/lectures')
def lectures():
	return render_template('lectures.html')


@app.route('/news')
def news():
	return render_template('news.html')


@app.route('/resources')
def resources():
	return render_template('resources.html')


@app.route('/tests')
def tests():
	return render_template('tests.html')
	
@app.route('/submit-login')
def login():
	
	#db = get_db()
	#db.row_factory = make_dicts
	#cur = db.cursor()

	#username = request.form['username']
	#password = request.form['password']
	#cur.close()
	#if (username == "Jeremy" and password == "password"):
	#	return 'You are now logged in!'

	return render_template('login.html')

@app.route('/submitLogin', methods=['POST'])
def submitLogin():
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run()
