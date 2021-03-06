from flask import Flask,jsonify,render_template,request,session,redirect,g
import os
import json
import sqlite3
from contextlib import closing

#configuration
DATABASE='./login_check.db'
SESSION_REFRESH_EACH_REQUEST=False

def connect_db():
	return sqlite3.connect(application.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
	        with application.open_resource('schema.sql', mode='r') as f:
	            db.cursor().executescript(f.read())
	        db.commit()


# create our applicationlication
application = Flask(__name__)
application.config.from_object(__name__)
application.secret_key=os.urandom(24)

init_db()		#initialises the database

registrations=[[] for x in range (5)]
# registrations[0] 	-- First Name
# registrations[1]	-- Last Name
# registrations[2]	-- username
# registrations[3]	-- password
# registrations[4]	-- Bio

@application.before_request
def before_request():
    g.db = connect_db()

@application.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@application.route('/password_match_end',methods=['GET','POST'])
def check_passwords():
	if request.method=="POST":
		parameters=request.data
		parameters=json.loads(parameters)
  		password = parameters['password']
		confirm_password = parameters['confirm_password']
		if password==confirm_password:
			password_matching_status=""
		else: 
			password_matching_status="Passwords do not match"
		return jsonify(result=password_matching_status)
	return jsonify(result="Wrong Method")

@application.route('/is_logged_in',methods=['POST'])
def is_logged_in():
	if not session.get('logged_in'):
		status="false"
	else :
		status="true"
	print jsonify(login_status=status)
	return jsonify(login_status=status)

@application.route('/profile_end',methods=['POST'])
def profile():
	if not session.get('logged_in'):
		firstname="error"
		lastname="error"
		bio="error"
		login_status="false"
	else :
		x=registrations[2].index(session['user'])
		firstname=registrations[0][x]
		lastname=registrations[1][x]
		bio=registrations[4][x]
		login_status="true"
	return jsonify(login_status=login_status,firstname=firstname,lastname=lastname,bio=bio)	

@application.route('/username_availability_end',methods=['GET','POST'])
def username_availability():
	if request.method=="POST":
		parameters=request.data
		parameters=json.loads(parameters)
		username=parameters['username']
		matches=[x for x in registrations[2] if x==username]
		if len(matches)==0:
			return jsonify(result="username available")
		return jsonify(result="username already exists")
	return jsonify(result="Wrong Method")

@application.route('/logout_end',methods=['POST'])
def logout():
	sid = request.cookies.get(application.session_cookie_name)
	print sid
	session.pop('logged_in',None)
	session.pop('user',None)
	g.db.execute("delete from login_status where session_id = ?",[sid])
	g.db.commit()
	return jsonify(status="logged out")

@application.route('/username_availability_for_login_end',methods=['GET','POST'])
def username_availability_for_login():
	if request.method=="POST":
		parameters=request.data
		parameters=json.loads(parameters)
		username=parameters['username']
		matches=[x for x in registrations[2] if x==username]
		if len(matches)==0:
			return jsonify(result="username does not exist")
		return jsonify(result="")
	return jsonify(result="Wrong Method")

@application.route('/login_attempt_end',methods=['GET','POST'])
def login_attempt():
	code=0
	if request.method=="POST":
		parameters=request.data
		parameters=json.loads(parameters)
		username=parameters['username']
		password = parameters['password']

		matches=[x for x in registrations[2] if x==username]
		if len(matches) == 0 :
			return jsonify(result="username doesn't exist",code=code)

		else :
			x=registrations[2].index(username)

			if registrations[3][x]==password :
				session['logged_in']=True
				session['user']=registrations[2][x]
				code=1
				if 'session' in request.cookies:
					print "Session there"
				else :
					print "Vedant"			
				return jsonify(result="Successfully loggged in",code=code)
			return jsonify(result="Incorrect credentials",code=code)
	return jsonify(result="Wrong Method",code=code)

@application.route('/store_in_database',methods=['POST'])
def store_in_database():
	sid = request.cookies.get(application.session_cookie_name)
	g.db.execute('insert into login_status (session_id, status) values (?, ?)', [sid,"logged_in"])
    	g.db.commit()
	return jsonify(status="successful")
	

@application.route('/registration_end',methods=['GET','POST'])
def registration():
	error=None
	if request.method=="POST":
		parameters=request.data
		parameters=json.loads(parameters)
		firstname=parameters['firstname']
		lastname=parameters['lastname']
		username=parameters['username']
		password = parameters['password']
		confirm_password = parameters['confirm_password']
		bio=parameters['input_text']
		
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
	application.run(debug=True)

