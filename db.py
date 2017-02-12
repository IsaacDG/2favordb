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
	responding_val = fields.Integer()
	picture = fields.String()
	category = fields.String()


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
	responding_fav = db.Column(db.Integer)
	picture = db.Column(db.String(2048))
	category = db.Column(db.String(128))

	def __init__(self,cid,rid,category,description,lat,lon,respfid,picture):
		self.completed = 0
		self.active = 0
		self.creator_id = cid
		self.responder_id = rid
		self.category = category
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


if __name__ == '__main__':
	# pprint(db.create_all())
	u = User(123, 'isaac', 'gonzalez', 'https://asdf.com')
	user_schema = UserSchema(many=True)
	pprint(user_schema.dump(User.query.all()).data)