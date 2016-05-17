from flask import Flask,jsonify,render_template,request,session,redirect
import os

# create our application
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key=os.urandom(24)

registrations=[[] for x in range (5)]
# registrations[0] 	-- First Name
# registrations[1]	-- Last Name
# registrations[2]	-- username
# registrations[3]	-- password
# registrations[4]	-- Bio

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login')
def login_page():
	return render_template('login.html')


@app.route('/register')
def register_page():
	print "Vedant"
	return render_template('register.html')

@app.route('/word_count')
def word_count_page():
	return render_template('word_count.html')

@app.route('/find_word_count',methods=['GET','POST'])
def find_word_count():
	if request.method=="POST":
		input_text=request.form['input_text']
		count=len(input_text)
		return jsonify(result=count)
	return jsonify(result="Wrong method")

@app.route('/password_match',methods=['GET','POST'])
def check_passwords():
	if request.method=="POST":
  		password = request.form['password']
		confirm_password = request.form['confirm_password']
		if password==confirm_password:
			password_matching_status=""
		else: 
			password_matching_status="Passwords do not match"
		return jsonify(result=password_matching_status)
	return jsonify(result="Wrong Method")

@app.route('/profile')
def profile():
	if not session.get('logged_in'):
		return 'You are not logged in'
	x=registrations[2].index(session['user'])
	firstname=registrations[0][x]
	lastname=registrations[1][x]
	bio=registrations[4][x]
	return render_template('profile.html',firstname=firstname,lastname=lastname,bio=bio)	

@app.route('/username_availability',methods=['GET','POST'])
def username_availability():
	if request.method=="POST":
		username=request.form['username']
		matches=[x for x in registrations[2] if x==username]
		if len(matches)==0:
			return jsonify(result="username available")
		return jsonify(result="username already exists")
	return jsonify(result="Wrong Method")

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	session.pop('user',None)
	return redirect('/')

@app.route('/username_availability_for_login',methods=['GET','POST'])
def username_availability_for_login():
	if request.method=="POST":
		username=request.form['username']
		matches=[x for x in registrations[2] if x==username]
		if len(matches)==0:
			return jsonify(result="username does not exist")
		return jsonify(result="")
	return jsonify(result="Wrong Method")

@app.route('/login_attempt',methods=['GET','POST'])
def login_attempt():
	if request.method=="POST":
		username=request.form['username']
		password = request.form['password']

		matches=[x for x in registrations[2] if x==username]
		if len(matches) == 0 :
			return jsonify(result="username already exists")

		else :
			x=registrations[2].index(username)

			if registrations[3][x]==password :
				session['logged_in']=True
				session['user']=registrations[2][x]
				return jsonify(result="Successfully loggged in")
			return jsonify(result="Incorrect credentials")
	return jsonify(result="Wrong Method")

@app.route('/registration',methods=['GET','POST'])
def registration():
	error=None
	if request.method=="POST":
		firstname=request.form['firstname']
		lastname=request.form['lastname']
		username=request.form['username']
		password = request.form['password']
		confirm_password = request.form['confirm_password']
		bio=request.form['input_text']
		
		if password!=confirm_password :
			error="Please review the entered details"
			return jsonify(result=error)
	
		else :
			matches=[x for x in registrations[2] if x==username]
			if len(matches) != 0 :
				error="Please review the entered details"
				return jsonify(result=error)
			else :	
				registrations[0].append(firstname)
				registrations[1].append(lastname)
				registrations[2].append(username)
				registrations[3].append(password)
				registrations[4].append(bio)
				return jsonify(result="Successfully registered")
	return jsonify(result="Wrong Method")	
	
if __name__=='__main__':
	app.run(debug=True)

