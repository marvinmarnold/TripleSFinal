
from flask import Flask, render_template, redirect, url_for, request, session
from sqlalchemy import create_engine
from database_setup import Base, User, Story
from sqlalchemy.orm import scoped_session, sessionmaker
import hashlib

engine = create_engine('sqlite:///flasky.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker())
app = Flask(__name__)
app.secret_key = 'super secret string'


def hash_password(password):
	return hashlib.md5(password.encode()).hexdigest()

def validate(name, password):
	query = DBSession.query(User).filter(User.name.in_([name]),User.password.in_([hash_password(password)]))
	return query.first() != None



@app.route('/', methods=['GET', 'POST'])
def signin():
	error = None
	if request.method == 'POST':
		name = str(request.form['username'])
		password = str(request.form['password'])
		is_valid = validate(name, password)
		if is_valid == False:
			error = 'Invalid credentials. Please try again.'
		else:
			session['name'] = name
			return redirect(url_for('home'))
	session['name'] = None
	return render_template('index.html', error = error)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup2.html')
	else:
		new_name = request.form['username']
		new_email = request.form['email']
		new_password = hash_password(request.form['password'])
		new_age = request.form['age']
		new_user= User(name=new_name,email=new_email,password=new_password,age = new_age)
		DBSession.add(new_user)
		DBSession.commit()
		session['name'] = new_name
		return redirect(url_for('home'))



@app.route('/home')
def home():
	name = session.get('name')
	if not name:
		return redirect(url_for('signin'))
	else:
		user=DBSession.query(User).filter_by(name = name).first()
		return render_template("home.html",user = user)

@app.route('/profile')
def profile():
	name = session.get('name')
	if not name:
		return redirect(url_for('signin'))
	else:
		user=DBSession.query(User).filter_by(name = name).first()
		return render_template("profile.html",user = user)

@app.route('/about')
def about():
	name = session.get('name')
	if not name:
		return redirect(url_for('signin'))
	else:
		user=DBSession.query(User).filter_by(name = name).first()
		return render_template("about.html",user = user)


@app.route('/story/<int:sid>')
def story(sid):
	name = session.get('name')
	if not name:
		return redirect(url_for('signin'))
	else:
		user=DBSession.query(User).filter_by(name = name).first()
		story = DBSession.query(Story).filter_by(id = sid).first()
		return render_template("story.html", story = story, user = user)






@app.route('/newstory', methods=['GET', 'POST'])
def newstory():
	if request.method == 'GET':
		return render_template('test.html')
	else:
		new_story=Story(name= 'The Inked Angel',writer='Shiran',story='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis feugiat faucibus luctus. Sed ante lacus, vehicula id enim ut, efficitur accumsan orci. Donec nec velit urna. Curabitur arcu risus, imperdiet ac malesuada et, maximus vitae enim. Donec a rutrum tortor. Aliquam eu quam malesuada, euismod velit sit amet, aliquet purus. Aenean pharetra orci a turpis elementum dapibus. Morbi accumsan finibus consequat. ',pic='img/story7.jpeg.jpeg')
		DBSession.add(new_story)
		DBSession.commit()
		return redirect(url_for('signin'))



if __name__=="__main__":
 	app.run()
