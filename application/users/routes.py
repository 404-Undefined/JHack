from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from application import bcrypt
from application.database import db
from application.models import User, Post, Submission
from application.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm, SubmissionForm)
from application.users.utils import save_picture, send_reset_email
import os
import random

users = Blueprint("users", __name__)

@users.route('/register', methods=["GET", "POST"])
def register():
	if current_user.is_authenticated: #if the user is already logged in
		return redirect(url_for("main.home")) #redirect the user back to the home page

	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data.encode("utf-8")).decode("utf-8")
		user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, age=form.age.data, password=hashed_password, role="Member") #pass in the UTF-8 hashed password, not the plain text nor binary
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

@users.route("/portal/<username>", methods=["GET", "POST"])
@login_required
def portal(username):
	if current_user.username != username:
		abort(403)

	page = request.args.get("page", 1, type=int) #site will throw ValueError if anything other than integer passed as page number. Default page of 1.
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4) #4 posts per page in descending order of date

	user = User.query.filter_by(username=username).first()
	team_submissions = [submission for submission in user.submission]

	return render_template("portal.html", posts=posts, user=current_user, team_submissions=team_submissions)


@users.route('/handle_code', methods=["GET", "POST"])
def handle_code():
	user = User.query.filter_by(username=current_user.username).first() #get the current user
	if user.submission: # user is already in a team
		flash("You are already in a team!", "warning")
	elif request.form["submit_button"] == "Join": # join an existing team
		team_code = request.form['code_input']
		team_submission = Submission.query.filter_by(code=int(team_code)).first()

		if team_submission is None:
			flash("This team does not exist yet. Create a team instead?", "warning")
		elif len(team_submission.team_member) >= 4:
			flash("This team is full! Create a new one?", "warning")
		else:
			team_submission.team_member.append(user)

			db.session.commit()
			flash(f"You have been added to the team {team_submission.team_name}!", "success")
	elif request.form["submit_button"] == "Create": # create a new team
		existing_codes = [submission.code for submission in Submission.query.all()] #list of all existing codes
		new_code = random.choice([x for x in range(100000, 1000000) if x not in existing_codes]) #generate a new 6 digit code

		new_team = Submission(code=new_code, team_name=f"{user.username}'s project")
		new_team.team_member.append(user) #add this user to the new team

		db.session.add(new_team)
		db.session.commit()

		flash(f"You have created a new team! Share this code {new_code} with your friends now!", "success")
	else:
		pass # unknown
	return redirect(url_for("users.portal", username=current_user.username))


@users.route("/submission/<team_code>", methods=["GET", "POST"])
@login_required
def submission(team_code):
	team_submission = Submission.query.filter_by(code=team_code).first()

	if not team_submission: # this team does not exist
		abort(404) #page not found error

	valid_usernames = [member.username for member in team_submission.team_member]

	if current_user.username not in valid_usernames: #team exists, but no permission
		abort(403) #permission denied error

	form = SubmissionForm()

	if form.validate_on_submit():
		team_submission.github = form.github.data
		team_submission.video = form.video.data
		team_submission.team_name = form.team_name.data
		team_submission.school_name = form.school_name.data
		team_submission.description = form.description.data
		team_submission.draft = form.draft.data

		db.session.commit()
		return redirect(url_for("users.portal", username=current_user.username))
	elif request.method == "GET":
		form.github.data = team_submission.github
		form.video.data = team_submission.video
		form.school_name.data = team_submission.school_name
		form.team_name.data = team_submission.team_name
		form.description.data = team_submission.description
		form.draft.data = team_submission.draft
	return render_template("submission.html", form=form, user=current_user)
