from flask import Flask, render_template, url_for, redirect, request, g, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
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



class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	#remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
	#email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

#User class, it's what we send and get from the database. Source: https://www.youtube.com/watch?v=8aTnmsDMldY
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	password = db.Column(db.String(80))
	
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
	
@app.route('/')
@app.route('/login')
def login():
	#db = get_db()
	#db.row_factory = make_dicts
	#cur = db.cursor()

	#username = request.form['username']
	#password = request.form['password']
	#cur.close()
	#if (username == "Jeremy" and password == "password"):
	#	return 'You are now logged in!'
	
	#Dummy login data
	
	
	return render_template('index.html')

@app.route('/submitLogin', methods=['POST'])
def submitLogin():
	#user = User.query.filter_by(username='Jeremy').first()
	db = get_db()
	db.row_factory = make_dicts
	cur = db.cursor()
	cur.close()
	username = request.form['username']
	password = request.form['password']
	
	user = query_db('select * from user where username = ?', [username], one=True)
	
	if user:		
		if (password == user['password']):
			if user["instructorBool"] == 0:
				session["GRADES"] = query_db('select * from marks where studentId = ?', [user["id"]], one=True)
			db.close()
			session["USER"] = user
			user = User.query.filter_by(username=username).first()		
			login_user(user)
			return redirect(url_for('home'))
	db.close()
	return render_template('failedLogin.html')
	
	
def registerUser(username, password, instructorBool):
	
	db = sqlite3.connect(DATABASE)
	db.row_factory = make_dicts
	cur2 = db.cursor()
	cur2.execute('insert into user (username, password, instructorBool) values (?, ?, ?)', [username, password, instructorBool])
	db.commit()
	cur2.close()
	db.close()
	

@app.route('/submitRegistration', methods=['POST'])
def submitRegister():

	db = get_db()
	db.row_factory = make_dicts
	cur = db.cursor()
	
	username = request.form['usernameRegister']
	userLogin2 = query_db('select * from user where username = ?', [username], one=True)
	cur.close()	
	db.commit()
	#db.close()
	
	if userLogin2:
		return '<h1>That username is already taken. Register with a different one.'
	
	password = request.form['passwordRegister']
	instructorRegister = request.form['instructorRegister']
	if instructorRegister == 'Instructor':
		instructorRegister2 = 1
	else:
		instructorRegister2 = 0
		
	
	registerUser(username, password, instructorRegister2)
	
	db = get_db()
	db.row_factory = make_dicts
	cur2 = db.cursor()
	userLogin = query_db('select * from user where username = ?', [username], one=True)
	cur2.close()
	db.close()
	if userLogin:
		if (password == userLogin['password']):
			
			user = userLogin
			session["USERNAME"] = user["username"]
			session["USER"] = user
			user = User.query.filter_by(username=username).first()		
			login_user(user)
			return redirect(url_for('home'))

	return render_template('failedLogin.html')
	
@app.route('/home')
@login_required
def home():
	
	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('home.html', user=session["USER"])
	
	return '<h1>Failed login. Unknown reason. </h1>'


@app.route('/signOut')
@login_required
def signOut():
	logout_user()
	session.pop("USER")
	return redirect(url_for('login'))
	
@app.route('/studentMarks')
@login_required
def studentMarks():

	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('studentMarks.html', user=session["USER"], grades=session["GRADES"])
	
	return '<h1>Failed login. Unknown reason. </h1>'

@app.route('/assignments')
@login_required
def assignments():

	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('assignments.html', user=session["USER"])
	
	return '<h1>Failed login. Unknown reason. </h1>'


@app.route('/calendar')
@login_required
def calendar():

	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('calendar.html', user=session["USER"])
	
	return '<h1>Failed login. Unknown reason. </h1>'
	
@app.route('/course_team')
@login_required
def course_team():

	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('course_team.html', user=session["USER"])
	
	return '<h1>Failed login. Unknown reason. </h1>'


@app.route('/feedback')
@login_required
def feedback():

	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('feedback.html', user=session["USER"])
	
	return '<h1>Failed login. Unknown reason. </h1>'


@app.route('/labs')
@login_required
def labs():

	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('labs.html', user=session["USER"])
	
	return '<h1>Failed login. Unknown reason. </h1>'


@app.route('/lectures')
@login_required
def lectures():

	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('lectures.html', user=session["USER"])
	
	return '<h1>Failed login. Unknown reason. </h1>'


@app.route('/news')
@login_required
def news():

	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('news.html', user=session["USER"])
	
	return '<h1>Failed login. Unknown reason. </h1>'


@app.route('/resources')
@login_required
def resources():

	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('resources.html', user=session["USER"])
	
	return '<h1>Failed login. Unknown reason. </h1>'


@app.route('/tests')
@login_required
def tests():

	#https://www.youtube.com/watch?v=PYILMiGxpAU this video about sessions
	
	return render_template('tests.html', user=session["USER"])
	
	return '<h1>Failed login. Unknown reason. </h1>'

if __name__ == '__main__':
	app.run()
