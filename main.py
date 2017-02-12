from flask import Flask
from flask import request
from oauth2client import client, crypt
from pprint import pprint
import json

from db import *


app = Flask(__name__)
#app.run(port=80)


def do_auth(better_data):
	pprint(better_data)
	CLIENT_ID = "711592045166-4o6ndv014o7l0jfq6dce74n3bh4l6o59.apps.googleusercontent.com"
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


@app.route('/search', methods=['POST'])
def search():
	data = json.loads(request.data)
	pprint(data)
	type = str(data['type'])
	pprint(type)
	#res = json.loads(do_auth(data))
	#if res['success'] is 1 or res['success'] == 1:

	if type == "all":
		return do_search_all()
	elif type == "tag":
		return do_search_tags(data['tags'])
	elif type == "loc":
		return do_search_loc(data['tags'])
	else:
		return "failure."

def do_search_all(data):
	favor_schema = FavorSchema(many=True)
	return json.loads(favor_schema.dump(Favor.query.all()).data)

def do_search_tags(tag_set):
	tags = tag_set.split(",")
	favor_schema = FavorSchema(many=True)
	q = db.session.query(Favor)
	res = q.filter(Favor.tags.any(Tag.name == tags[0]))
	for tag in tags:
		res2 = q.filter(Favor.tags.any(Tag.name == tag))
		for d in res2:
			print res2.__dict__
		# this doesn't work!!! in fact, i'm annoyed because tags... but you sould be able to do 
	 #       favor_schema = FavorSchema(many=True)
       	#  return json.loads(favor_schema.dump(Favor.query.all(id=data['cid'])).data)
		#res = [list(filter(lambda x: x in res, sublist)) for sublist in res2]

	return json.loads(favor_schema.dump(res).data)

def do_search_loc(data, lat, lon, range):
	sql = "SELECT id,creator_id,responder_id,tags,description,active,completed," \
	"lat,lon,responding_val,picture,category, (6371 * ACOS( COS( RADIANS( :lat ) ) " \
	"* COS( RADIANS( lat ) )* COS( RADIANS( lon ) - RADIANS( :lon ) )+ " \
	"SIN( RADIANS( :lat ) ) * SIN( RADIANS( lat ) ) )) AS distance " \
	"FROM favor ORDER BY distance where distance < :dst"

	ans = db.session.query.from_statement(sql).params(lat=lat,lon=lon,dst=range)
	pprint(ans)
	return ""


@app.route("/favor")
def process_favor(pe):
	# if we win, i don't want any of the prize or credit, didn't do enough to be helpful or worth the credit.
	# feel bad for slowing you guys down.
	data = json.loads(request.data)
	type = str(data['type'])
	res = json.loads(do_auth(data))
	if res:
		if type == "info":
			# get the data
			# unfun, because we have to use deseralization to get it to json...
			favor_schema = FavorSchema(many=True)
        		return json.loads(favor_schema.dump(Favor.query.all(id=data['cid'])).data)
		elif type == "add":
			# insert
			f = Favor(data['cid'],data['rid'],data['title'],data['desc'],data['lat'],data['lon'],data['responder_id'],data['picture'])
			db.session.add(f)
			db.session.commit()
			return json.dumps({'type': 'favor', 'success': 1})
		elif type == "complete":
			# edit
			cu = User.query.filter_by(id=int(data['cid'])).first()
			cu.active = 0
			cu.completed = 1
			db.session.commit()
			return json.dumps({'type': 'favor', 'success': 1})
		elif type == "select":
			# from the perspective of the selecting user, they pick a favor created by someone else. 
			# they then are put as responderid waiting for it to become active
			# if I had more time, I'd rewrite this stuff in a queue
			cu = User.query.filter_by(id=int(data['cid'])).first()
			ru = User.query.filter_By(id=int(data['rid'])).first()
			cu.responder_id = data['rid']
			ru.responder_id = data['cid']
			db.session.commmit()
			return json.dumps({'type': 'favor', 'success': 1})
		elif type == "accept":
			# like above, but this time we set the activeness on both
			# but to make this work better without hard coding a swap of users upon pick (which is very bad)
			# we should separate these calls out more, so an accept can be requested by a single user, and the other user can accept someone else. but has to accept someone to be active.
			cu = User.query.filter_by(id=int(data['cid'])).first()
			ru = User.query.filter_By(id=int(data['rid'])).first()
			cu.active = 1
			ru.active = 1
			db.session.commit()
			return json.dumps({'type': 'favor', 'success': 1})
		elif type == "decline":
			# edit the other and mark as active....
			cu = User.query.filter_by(id=int(data['cid'])).first()
			ru = User.query.filter_By(id=int(data['rid'])).first()
			cu.responder_id = 0
			ru.responder_id = 0
			cu.active = 0
			db.session.commit()
			return json.dumps({'type': 'favor', 'success': 1})
		else:
			return json.dumps({'type': 'favor', 'success': 0})
@app.route("/")
def root():
	return "<p>Nothing to see here...</p>"

@app.route('/auth', methods=['POST'])
def login():
	if request.method == 'POST':
		return do_auth(json.loads(request.data))
	else:
		return "lol!"

#this is for tags, but i don't think we use it anymore bye bye 
@app.route("/category/<act>", methods=['POST', 'GET'])
def category(act):
	# check if its add or remove
	print("hi")

if __name__ == "__main__":
    app.run()
