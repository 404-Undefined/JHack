from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from tzlocal import get_localzone
from application import login_manager, admin
from application.database import db
from flask_login import UserMixin, current_user
from flask import current_app
from flask_admin.contrib.sqla import ModelView

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	first_name = db.Column(db.String(20),  unique=False, nullable=True)
	last_name = db.Column(db.String(20), unique=False, nullable=True)
	age = db.Column(db.Integer, nullable=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	responsibility = db.Column(db.Text, nullable=True)
	password = db.Column(db.String(60), nullable=False)
	role = db.Column(db.String(10), default="Member")
	submission = db.relationship("Submission", secondary="user_submission", backref="team_member", lazy=True) #Submission.team_member
	date_joined = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

	def get_reset_token(self, expires_seconds=1800):
		serializer_obj = Serializer(current_app.config["SECRET_KEY"], expires_seconds)
		return serializer_obj.dumps({"user_id": self.id}).decode()

	@staticmethod
	def verify_reset_token(token):
		serializer_obj = Serializer(current_app.config["SECRET_KEY"])
		try: 
			user_id = serializer_obj.loads(token)["user_id"]
		except: #token expired. itsdangerous.exc.SignatureExpired: Signature expired
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User({self.username}, {self.email}, {self.first_name}, {self.last_name}, {self.role})"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f"Post({self.title}, {self.date_posted} {self.content})"

class Workshop(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f"Workshop({self.title}, {self.date_posted} {self.content})"

class SubscribedUser(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)

class Submission(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.Integer, nullable=True) #6 digit code/id. Make this the primary key?
	team_name = db.Column(db.String(100), nullable=True)
	school_name = db.Column(db.String(100), nullable=True)
	video = db.Column(db.String(100), nullable=True)
	github = db.Column(db.String(100), nullable=True)
	description = db.Column(db.String(), nullable=True)
	editable = db.Column(db.Boolean, default=True)
	draft = db.Column(db.Boolean, default=True, nullable=True)

	def __repr__(self):
		return f"Submission({self.code}, {self.team_name}, {self.team_member}, draft: {self.draft})"

class UserSubmission(db.Model):
    __tablename__ = 'user_submission'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    submission_id = db.Column(db.Integer(), db.ForeignKey('submission.id'))

class UserSubmissionView(ModelView):
    column_hide_backrefs = False
    column_list = ('username', 'email', 'age', 'submission')
    def is_accessible(self):
    	return current_user.is_authenticated and current_user.role == "Admin" 

class MyModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.role == "Admin" 

admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(SubscribedUser, db.session))
admin.add_view(MyModelView(Submission, db. session))
admin.add_view(UserSubmissionView(User, db.session))
