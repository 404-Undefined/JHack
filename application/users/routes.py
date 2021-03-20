from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from application import bcrypt
from application.database import db
from application.models import User, Post, Submission
from application.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, SubmissionForm)
from application.users.utils import save_picture, send_reset_email
import os

users = Blueprint("users", __name__)

@users.route('/register', methods=["GET", "POST"])
def register():
	if current_user.is_authenticated: #if the user is already logged in
		return redirect(url_for("main.home")) #redirect the user back to the home page

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data.encode("utf-8")).decode("utf-8")
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, bio="", gender="", role="Member") #pass in the UTF-8 hashed password, not the plain text nor binary
		db.session.add(user)
		db.session.commit()

		flash(f"Account created for {form.username.data}!", "success") #bootstrap class category: success, danger, etc
		return redirect(url_for("users.login"))
	return render_template("register.html", title="Register", form=form)

@users.route('/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated: #if the user is already logged in
		return redirect(url_for("main.home")) #redirect the user back to the home page
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first() #check if there are any emails within our database matching the email that the user entered
		if user and bcrypt.check_password_hash(user.password, form.password.data): #if the email exists and the password hash is valid
			login_user(user, remember=form.remember.data)

			#If the user tried to access a log-in only page and was redirected to /login, then automaticall send the user back to where they were going.
			next_page = request.args.get("next") #args is a dictionary but use args.get() not args[] because [] will throw an error if the key does not exist
			return redirect(next_page) if next_page else redirect(url_for("main.home"))
		else: #login is unsuccessful
			flash("Invalid!", "danger") #danger alert (Bootstrap)
	return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("main.home"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_filename = save_picture(form.picture.data)
			current_user.image_file = picture_filename
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.bio = form.bio.data if form.bio.data else ""
		current_user.gender = form.gender.data if form.gender.data else ""
		db.session.commit()
		flash("Your account has been updated", "success")
		return redirect(url_for("users.account"))
	elif request.method == "GET": #populate the form fields with the user's existing data
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.bio.data = current_user.bio
		form.gender.data = current_user.gender
	return render_template("account.html", title="Account", form=form)

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))	
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash("An email has been sent with instructions to reset your password.", "info")
		return redirect(url_for("users.login"))

	return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for("main.home"))

	user = User.verify_reset_token(token)
	if not user:
		flash("The token is invalid or expired.", "warning")
		return redirect(url_for("users.reset_request"))

	form = ResetPasswordForm()

	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user.password = hashed_password
		db.session.commit()
		flash(f"Your password has been updated!", "success")
		return redirect(url_for("users.login"))
	return render_template("reset_password.html", title="Reset Password", form=form)

@users.route("/portal/<username>")
@login_required
def portal(username):
	if current_user.username != username:
		abort(403)

	page = request.args.get("page", 1, type=int) #site will throw ValueError if anything other than integer passed as page number. Default page of 1.
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4) #4 posts per page in descending order of date
	return render_template("portal.html", posts=posts, user=current_user)

@users.route("/submission/<username>", methods=["GET", "POST"])
@login_required
def submission(username):
	if current_user.username != username:
		abort(403)

	submission = Submission.query.filter_by(creator=current_user).first()

	form = SubmissionForm()
	if form.validate_on_submit():
		if submission is not None:
			submission.github = form.github.data
			submission.video = form.video.data
			submission.team_name = form.team_name.data
			submission.school_name = form.school_name.data
			submission.description = form.description.data
		else: # create new submission
			new_submission = Submission(user_id=current_user.id, github=form.github.data, video=form.video.data, team_name=form.team_name.data,\
				school_name=form.school_name.data, description=form.description.data)
			db.session.add(new_submission)

		db.session.commit()
		return redirect(url_for("users.portal", username=current_user.username))
	elif request.method == "GET":
		if submission is not None: # if the user has already started a submission, then pre-fill 
			form.github.data = submission.github
			form.video.data = submission.video
			form.school_name.data = submission.school_name
			form.team_name.data = submission.team_name
			form.description.data = submission.description
	return render_template("submission.html", form=form, user=current_user)
