import flask
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint

app = flask.Flask(__name__)
app.config['SQL_DATABASE_URI'] = 'mysql://root:134890f20194j2309cj@localhost/favors'
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQL_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

tags = db.Table('tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
	db.Column('favor_id', db.Integer, db.ForeignKey('favor.id'))
)

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

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	display_first = db.Column(db.Unicode(100))
	display_last = db.Column(db.Unicode(100))
	profile_picture = db.Column(db.String(2048))

	def __init__(fname,lname,pp):
		self.display_First = fname
		self.display_last = lname
		self.profile_picture = pp

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)

if __name__ == '__main__':
	pprint(db.create_all())
