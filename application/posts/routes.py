from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from application.database import db
from application.models import Post
from application.posts.forms import PostForm
from application.posts.utils import save_image
import markdown2
import os
import secrets
from datetime import datetime
from tzlocal import get_localzone
from sqlalchemy import func

posts = Blueprint("posts", __name__)

@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
	#only admins can create posts
	if current_user.role != "Admin":
		abort(403)

	form = PostForm()
	if form.validate_on_submit():			
		post = Post(title=form.title.data, content=form.content.data)

		db.session.add(post)
		db.session.commit()
		flash(f"Your post has been created!", "success")
		return redirect(url_for("posts.post", post_id=post.id))

	return render_template("create_post.html", title="New Post", form=form)

@posts.route('/post/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)

	#only admins can edit posts
	if currrent_user.role != "Admin":
		abort(403)

	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data

		db.session.commit() #We're updating something that is already in the database, so no need for db.session.add()
		flash("The post has been updated!", "success")
		return redirect(url_for("posts.post", post_id=post.id))
	elif request.method == "GET": #when update post page is loaded, pre-fill title and content with existing data
		form.title.data = post.title
		form.content.data = post.content
	return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")

@posts.route('/post/<int:post_id>/delete', methods=["POST"])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)

	#only admins can delete postss
	if currrent_user.role != "Admin":
		abort(403)

	db.session.delete(post)
	db.session.commit()
	flash("Your post has been deleted!", "success")
	return redirect(url_for("main.home"))

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
