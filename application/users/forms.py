from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, FormField, FieldList, Form, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional, URL
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets
from flask_login import current_user
from application.models import User, Submission

class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")]) #Confirm password must be equal to password
	first_name = StringField("First Name", validators=[DataRequired(Length(min=1, max=20))])
	last_name = StringField("Last Name", validators=[DataRequired(Length(min=1, max=30))])
	age = h5fields.IntegerField("Age", validators=[DataRequired()], widget=h5widgets.NumberInput(min=1, max=100, step=1))
	submit = SubmitField("Register")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first() #if user exists - if not, None
		if user:
			raise ValidationError("This username is taken.")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first() #if email exists - if not, None
		if user:
			raise ValidationError("This email is taken.")


class LoginForm(FlaskForm):
 	email = StringField("Email", validators=[DataRequired(), Email()])
 	password = PasswordField("Password", validators=[DataRequired()])
 	remember = BooleanField("Remember Me")
 	submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	picture = FileField("Profile Picture", validators=[FileAllowed(["jpg", "png"])])
	gender = RadioField("Gender", choices=[("Male", "Male"), ("Female", "Female"), ("Prefer not to say", "Prefer not to say")], validators=[Optional()])
	bio = TextAreaField("Bio", validators=[Optional(), Length(max=200)])
	submit = SubmitField("Update")

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("This username is taken.")

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("This email is taken.")

class RequestResetForm(FlaskForm):
	email = StringField("Email", validators=[DataRequired(), Email()])
	submit = SubmitField("Request Password Reset")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError("There is no account with this email. Please register first.")

class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Reset Password")

class SubmissionForm(FlaskForm):
	team_name = StringField("Team Name", validators=[DataRequired()])
	school_name = StringField("School Name", validators=[DataRequired()])
	github = StringField("GitHub Repository URL (optional)")
	description = TextAreaField("Description", default="""
	<p class="questiont-text">What does your project do?</p>
	<p class="questiont-text">What tools/programming languages did you use?</p>
	<p class="questiont-text">Challenges that you faced</p>
	<p class="questiont-text">Optional improvements/extensions to your project</p>""")
	video = StringField("Video URL (optional)")
	submit = SubmitField("Submit")
	draft = BooleanField("Draft (uncheck to submit)", default=True)
