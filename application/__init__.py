from flask import Flask
from application.config import Config
from application.database import db, migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_s3 import FlaskS3
from flask_talisman import Talisman
from application.posts.momentjs import momentjs

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login" #pass in the function name of the login route
login_manager.login_message_category = "info" #Styles "Please log in to view this page" with Bootstrap "info" class
admin = Admin()
mail = Mail()
s3 = FlaskS3()
talisman = Talisman()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	@app.context_processor
	def context_processor():
		return dict(momentjs=momentjs)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	admin.init_app(app)
	s3.init_app(app)
	migrate.init_app(app, db, render_as_batch=True)
	talisman.init_app(app, content_security_policy=None)

	from application.main.routes import main
	from application.users.routes import users
	from application.posts.routes import posts
	from application.commands import cmd
	app.register_blueprint(main)
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(cmd)

	return app
