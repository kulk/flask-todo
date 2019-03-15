from app import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	tasks = db.relationship('Task', backref='author', lazy='dynamic') # allows a user.tasks query, the backref allows a task.author query

	def __repr__(self):
		return '<User %s>' % self.email

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(160))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user is the name of the table of the user model
