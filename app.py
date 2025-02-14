
from flask import Flask, render_template, redirect, url_for, request, session
from sqlalchemy import create_engine
from database_setup import User, Story, DBSession
import hashlib




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


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404



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






@app.route('/somerandomstufftoaddstories', methods=['GET', 'POST'])
def newstory():
	if request.method == 'GET':
		return render_template('test.html')
	else:
		new_name = request.form['username']
		new_writer = request.form['email']
		new_content = request.form['password']
		new_pic = request.form['age']
		new_story=Story(name= new_name,writer=new_writer, story= new_content , pic= new_pic)
		DBSession.add(new_story)
		DBSession.commit()
		return redirect(url_for('signin'))



if __name__=="__main__":
 	app.run(host = "0.0.0.0",debug = True)
