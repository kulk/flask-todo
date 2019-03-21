from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	tasks = db.relationship('Task', backref='author', lazy='dynamic') # allows a user.tasks query, the backref allows a task.author query

	def __repr__(self):
		return '<User %s>' % self.email

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Task(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(160))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # user is the name of the table of the user model

@login.user_loader
def load_user(id):
	return User.query.get(int(id))