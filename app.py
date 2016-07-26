
from sqlalchemy.orm import *
from flask import *
from sqlalchemy import create_engine
from database_setup import Base, User
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('sqlite:///flasky.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

#DBSessionMaker = sessionmaker(bind=engine)
#DBSession = DBSessionMaker()
DBSession = scoped_session(sessionmaker())
app = Flask(__name__)
def hash_password(password):
	return hashlib.md5(password.encode()).hexdigest()

def validate(name, password):
	print('in validate')
	query = DBSession.query(User)#.filter(User.name.in_([name]),User.password.in_([hash_password(password)]))
	print('after query')
	return query.first() != None



@app.route('/')
def welcome():
 	return render_template("welcome.html")



@app.route('/signin', methods=['GET', 'POST'])
def signin():
	error = None
	if request.method == 'POST':
		name = str(request.form['username'])
		password = str(request.form['password'])
		print('pre validate')
		is_valid = validate(name, password)
		print('1')
		if is_valid == False:
			print('1')
			error = 'Invalid credentials. Please try again.'
		else:
			print('2')
			session['name'] = name
			print('2')
			return redirect(url_for('lhome'))
			print('3')
	print('4')
	return render_template('signin.html', error = error)




@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
	else:
		new_name = request.form['username']
		new_email = request.form['email']
		new_password = hash_password(request.form['password'])
		new_age = request.form['age']
		new_user= User(name=new_name,email=new_email,password=new_password,age = new_age)
		DBSession.add(new_user)
		DBSession.commit()
		print('0')
		session['name'] = name
		print('1')
		return redirect(url_for('lhome'))
		print('2')

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
	name = session.get('name')
	if not name:
		return redirect(url_for('signin'))
	else:
		return render_template('lhome', name = name)



@app.route('/profile')
def profile():
	return render_template("profile.html")

if __name__=="__main__":
 	app.run()
