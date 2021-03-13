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
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default="default.jpg") #user's profile picture
	password = db.Column(db.String(60), nullable=False)
	bio = db.Column(db.String(400))
	gender = db.Column(db.String(20))
	role = db.Column(db.String(10), default="Member")

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
		return f"User({self.username}, {self.email}, {self.gender}, {self.bio}, {self.image_file})"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f"Post({self.title}, {self.date_posted} {self.content})"

class SubscribedUser(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)

class MyModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.role == "Admin"

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(SubscribedUser, db.session))