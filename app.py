from flask import Flask, render_template, request, redirect,url_for
app = Flask(__name__)

from database_setup import Base, User,Story
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///crudlab.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def hash_password(password):
	return hashlib.md5(password.encode()).hexdigest()

def validate(name, password):
	query = DBSession.query(User).filter(User.name.in_([name]),User.password.in_([hash_password(password)]))
	return query.first() != None



@app.route('/')
def welcome():
 	return render_template("welcome.html")



@app.route('/signin', methods=['GET', 'POST'])
def signin():
	error = None
	if request.method == 'POST':
		name = str(request.form['username'])
		passwrd = str(request.form['password'])
		if is_valid == False:
			error = 'Invalid credentials. Please try again.'
		else:
			session['name'] = name
			return redirect(url_for('lhome'))
	return render_template('signin.html', error = error)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
	else:
		new_name = request.form['username']
		#exists = db.session.query(User.id).filter_by(name='new_name').scalar() is not None
		#print("1")
		#if exists == 0 :
		new_email = request.form['email']
		new_password = request.form['password']
		new_age = request.form['age']
		new_user= User(name=new_name,email=new_email,password=new_password,age = new_age)
		session.add(new_user)
		session.commit()
		session['name'] = name
		return redirect(url_for('lhome'))
		#else:
			#print ('user name taken')

@app.route('/contact')
def contact():
	return render_template("contact.html")

@app.route('/home')
def home():
	return render_template("home.html")

@app.route('/fullstory')
def fullstory():
 	return render_template("fullstory.html")


@app.route('/lhome')
def lhome():
	name = sesion.get('name')
	if not name:
		return redirect(url_for('signin'))
	else:
		return render_template('lhome', name = name)



@app.route('/profile')
def profile():
	return render_template("profile.html")

if __name__=="__main__":
 	app.run()
