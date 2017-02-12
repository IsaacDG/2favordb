import flask
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config['SQL_DATABASE_URI'] = 'sqlite:////tmp/test.db'
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
	description = db.Column(db.Unicode)
	active = db.Column(db.Boolean)
	completed = db.Column(db.Boolean)
	lat = db.Column(db.Float)
	lon = db.Column(db.Float)
	responding_fav = db.Column(db.Integer)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	display_name = db.Column(db.Unicode)


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)





