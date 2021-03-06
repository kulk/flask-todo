from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, TodoForm, RegistrationForm
from app.models import User, Task


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = TodoForm()
	tasks = current_user.tasks
	if form.validate_on_submit():
		task = Task(body=form.task.data, author=current_user)
		db.session.add(task)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('index.html', form=form, tasks=tasks)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
	task_id = request.form.get('task_id') # Gets the id of Task from the form
	delete_task = Task.query.filter_by(id=task_id).first() # query to find the task based on the id
	db.session.delete(delete_task)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST']) # Create login route
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)