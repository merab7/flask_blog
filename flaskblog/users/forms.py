from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,  PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length,  EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user




class Registration_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20) ])
    email = EmailField('Email', validators=[DataRequired(), Length(min=8)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username already exists')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already in use.')
        


class Login_form(FlaskForm):
    email = EmailField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')





class Update_account(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=20) ])
    email = EmailField('Email', validators=[DataRequired(), Length(min=8)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    def validate_username(self, username):
         if username.data != current_user.username:   
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username already exists')
            
            
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email already in use.')
            

            

class RequestResetForm(FlaskForm):
     email = EmailField('Email', validators=[DataRequired(), Length(min=8)])
     submit = SubmitField('Request Password Reset')

     def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email ')
        



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')               
        