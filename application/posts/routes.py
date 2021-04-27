from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from application.database import db
from application.models import Post, Workshop
from tzlocal import get_localzone

posts = Blueprint("posts", __name__)

@posts.route("/create_post")
@login_required
def create_post():
	if current_user.role != "Admin":
		abort(403)
	return render_template("create_post.html")

@posts.route("/create_workshop")
@login_required
def create_workshop():
	if current_user.role != "Admin":
		abort(403)
	return render_template("create_workshop.html")

@posts.route("/handle_create_post", methods=["GET", "POST"])
@login_required
def handle_create_post():
	if current_user.role != "Admin":
		abort(403)

	title = request.form["title"]
	content = request.form["content"]
	post = Post(title=title, content=content)

	db.session.add(post)
	db.session.commit()
	return redirect(url_for("main.home"))

@posts.route("/handle_create_workshop", methods=["GET", "POST"])
@login_required
def handle_create_workshop():
	if current_user.role != "Admin":
		abort(403)

	title = request.form["title"]
	content = request.form["content"]
	post = Workshop(title=title, content=content)

	db.session.add(post)
	db.session.commit()
	return redirect(url_for("main.home"))
