from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, MultipleFileField
from wtforms.validators import DataRequired, Optional
class PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = TextAreaField("Content", validators=[DataRequired()])
	draft = BooleanField("Draft", validators=[Optional()])
	attachments = MultipleFileField("Attached Files")
	submit = SubmitField("Post")