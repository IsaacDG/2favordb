import flask
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
from json import JSONEncoder
import json
from marshmallow import Schema, fields

app = flask.Flask(__name__)
app.config['SQL_DATABASE_URI'] = 'mysql://root:134890f20194j2309cj@localhost/favors'
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQL_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

tags = db.Table('tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
	db.Column('favor_id', db.Integer, db.ForeignKey('favor.id'))
)

class TagSchema(Schema):
	id = fields.Integer()
	name = fields.String()

class FavorSchema(Schema):
	id = fields.Integer()
	creator_id = fields.Integer()
	responder_id = fields.Integer()
	tags = fields.Nested(TagSchema)
	description = fields.String()
	active = fields.Boolean()
	completed = fields.Boolean()
	lat = fields.Float()
	lon = fields.Float()
	responding_fav = fields.Integer()
	picture = fields.String()
	category = fields.String()
	title = fields.String()

class Favor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	creator_id = db.Column(db.Integer)
	responder_id = db.Column(db.Integer)
	tags = db.relationship('Tag', secondary=tags,
		backref=db.backref('favors', lazy='dynamic'))
	description = db.Column(db.String(32768))
	active = db.Column(db.Boolean)
	completed = db.Column(db.Boolean)
	lat = db.Column(db.Float)
	lon = db.Column(db.Float)
	title = db.Column(db.String(255))
	responding_fav = db.Column(db.Integer)
	picture = db.Column(db.String(2048))
	category = db.Column(db.String(128))

	def __init__(self,cid,rid,title,description,lat,lon,respfid,picture):
		self.completed = 0
		self.active = 0
		self.creator_id = cid
		self.responder_id = rid
		self.title = title
		self.description = description
		self.lat = lat
		self.lon = lon
		self.responding_fav = respfid
		self.picture = picture



class UserSchema(Schema):
    id = fields.Integer()
    uid = fields.Integer()
    display_first = fields.String()
    display_last = fields.String()
    profile_picture = fields.String()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer())
	display_first = db.Column(db.String(100))
	display_last = db.Column(db.String(100))
	profile_picture = db.Column(db.String(2048))

	def __init__(self, uid, fname,lname,pp):
		self.display_first = fname
		self.display_last = lname
		self.profile_picture = pp
		self.uid = uid

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), unique=True)

	def __init__(self,tag):
		self.name = tag

if __name__ == '__main__':
	from random import randint as random
	#pprint(db.create_all())
	#u = User(random(1,100), 'isaac', 'gonzalez', 'https://asdf.com')
	#db.session.add(u)
	#db.session.commit()
	#a = Favor(random(1,200),random(1,200),'a,b,c,d,e,d','the quick brown fox jumped over the lazy dog',113.111231,37.1112,random(1,200),'http://google.om')
	#a.tags.append(Tag('Sex'))
	#a.tags.append(Tag('Drugs'))
	#a.tags.append(Tag('Rock'))
	#db.session.add(a)
	#db.session.commit()
