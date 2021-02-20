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

allowed_formats = [".jpg", ".jpeg", ".png", ".tiff", ".mp4", ".gif"]

@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
	#only admins can create posts
	if current_user.role != "Admin":
		abort(403)

	form = PostForm()
	if form.validate_on_submit():
		content = form.content.data
		attachments = request.files.getlist(form.attachments.name)

		if attachments and all(f for f in attachments):
			for attachment in attachments:
				_, file_extension = os.path.splitext(attachment.filename)
				if file_extension in allowed_formats:
					saved_image_path = save_image(attachment)
					content = content.replace(attachment.filename, saved_image_path)
				else:
					flash(f"{attachment.filename}: This file is not supported.", "warning")
		# content = markdown2.markdown(content)

		post = Post(title=form.title.data, content=content, author=current_user, draft=int(form.draft.data))

		for tag_name in form.tags.data:
			tag = Tag.query.filter_by(name=tag_name).first()
			if tag_name == "Daily Digest": #clear all other tags with daily digest tag
				tag.posts = []
			tag.posts.append(post)

		db.session.add(post)
		db.session.commit()
		flash(f"Your post has been created! {form.draft.data} {type(form.draft.data)}", "success")
		return redirect(url_for("posts.post", post_id=post.id))

	return render_template("create_post.html", title="New Post", form=form)

@posts.route('/post/<int:post_id>', methods=["GET", "POST"])
def post(post_id):
	post = Post.query.get_or_404(post_id) #return post with this id; if it doesn't, return 404
	recent_posts = Post.query.filter(Post.draft == 0, Post.id != post_id).order_by(func.random()).limit(3).all()

	return render_template("post.html", title=post.title, post=post, recent_posts=recent_posts)

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
		post.draft = int(form.draft.data)

		content = form.content.data
		attachments = request.files.getlist(form.attachments.name)

		if attachments and all(f for f in attachments):
			for attachment in attachments:
				_, file_extension = os.path.splitext(attachment.filename)
				if file_extension in allowed_formats:
					saved_image_path = save_image(attachment)
					content = content.replace(attachment.filename, saved_image_path)
				else:
					flash(f"{attachment.filename}: This file is not supported.", "warning")
		post.content = content
		# post.content = markdown2.markdown(content)

		db.session.commit() #We're updating something that is already in the database, so no need for db.session.add()
		flash("The post has been updated!", "success")
		return redirect(url_for("posts.post", post_id=post.id))
	elif request.method == "GET":
		form.title.data = post.title
		form.content.data = post.content
		form.draft.data = post.draft
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