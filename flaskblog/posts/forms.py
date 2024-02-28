from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField





class Post_form(FlaskForm):
      title = StringField('Title', validators=[DataRequired()])
      content = CKEditorField("Blog Content", validators=[DataRequired()])
      post = SubmitField('Post')


class Edit_form(FlaskForm):
      title = StringField('Title', validators=[DataRequired()])
      content = CKEditorField("Blog Content", validators=[DataRequired()])
      post = SubmitField('Update')