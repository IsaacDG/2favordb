from flask import Flask
from flask import request
from oauth2client import client, crypt
from pprint import pprint
import json

from db import *


app = Flask(__name__)
#app.run(port=80)

def do_auth(data):
	CLIENT_ID = "711592045166-4o6ndv014o7l0jfq6dce74n3bh4l6o59.apps.googleusercontent.com"
	better_data = json.loads(data)
	pprint(better_data)
	token = str(better_data['token'])
	try:
		idinfo = client.verify_id_token(token, CLIENT_ID)
		if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
			raise crypt.AppIdentityError("Wrong issuer.")
			print("Wrong Issuer.") 
		else:
			print("Beginning query for authen")
			# do we add a user ? i don't know. we could try
			usr = User.query.filter_by(uid=int(idinfo['sub']))
			pprint(usr)
			if usr is None or usr.count() < 0:
				print("User is not in count! Attemping to add")
				# add user
				u = User(int(idinfo['sub']),idinfo['family_name'], idinfo['given_name'], idinfo['picture'])
				db.session.add(u)
				db.session.commit()
				return json.dumps({'type': 'auth', 'success': 1})
			else:
				print("User exists... now what?")
				return json.dumps({'type': 'auth', 'success': 1})
		return json.dumps({'type': 'auth', 'success': 0})
	except crypt.AppIdentityError:
		return json.dumps({'type': 'auth', 'success': 0})

@app.route('/search/<type>')
def search(type, request):
	if request.method == 'POST':
		if type is "all":
			return do_search_all(request.data)
		elif type is "tags":
			return do_search_tags(request.data)
		elif type is "loc":
			return do_search_loc(request.data)
		else:
			return "f"
	else:
		return "f"

def do_search_all(data):
	return ""

def do_search_tags(data):
	return ""

def do_search_loc(data):
	return ""

@app.route("/")
def root():
	return "<p>Nothing to see here...</p>"

@app.route("/info/<favor>")
def info(favor):
	iff = int(favor) # read an integer
	return iff

@app.route('/auth', methods=['POST'])
def login():
	if request.method == 'POST':
		return do_auth(request.data)
	else:
		return "lol!"

@app.route("/category/<act>", methods=['POST', 'GET'])
def category(act):
	# check if its add or remove
	print("hi")

if __name__ == "__main__":
    app.run()
