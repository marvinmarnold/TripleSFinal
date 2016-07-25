from flask import Flask, render_template, request, redirect,url_for
app = Flask(__name__)

from database_setup import Base, User,Story
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///crudlab.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def welcome():
 	return render_template("welcome.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if request.method == 'GET':
		return render_template('signin.html')
	else:
		loger = session.query(User).filter_by(name = request.form['username']).first()
		print(loger)
		if request.form['username'] == loger.name :
			print ('after username')
			if loger.password == request.form['password'] :
				print ('after password')
				return redirect(url_for('lhome',uid=loger.id))
				print ('after redirect')
			else:
				print('wrong pass')
				#wrong password

		else:
			print('didnt signup')
			#you didnt sign up



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
		return redirect(url_for('lhome',uid=new_user.id))
		#else:
			#print ('user name taken')

@app.route('/contact')
def contact():
	return render_template("contact.html")

@app.route('/home')
def home():
	return render_template("home.html")




@app.route('/lhome/<uid>')
def lhome(uid):
	user = session.query(User).filter_by(id = uid).first()
	return render_template("lhome.html", user=user)

@app.route('/profile')
def profile():
	return render_template("profile.html")

if __name__=="__main__":
 	app.run()
