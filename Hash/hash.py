#all the imports
import sqlite3, md5
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify


# create our application
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/password_match')
def check_passwords():
  	password = request.args.get('password')
	confirm_password = request.args.get('confirm_password')
	if password==confirm_password:
		password_matching_status=""
	else: 
		password_matching_status="Passwords do not match"
	return jsonify(result=password_matching_status)

@app.route('/hash_the_string')
def hash_the_string():
  	string = request.args.get('username')
	hashed_string=md5.new()
	hashed_string.update(string)
	return jsonify(result=hashed_string.hexdigest())


if __name__=='__main__':
	app.run(debug=True)
