from flask import   url_for, current_app
from flaskblog import  mail
import secrets
import os
from PIL import Image
from flask_mail import Message



def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_fname = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fname )
    
    #resize image with pil 
    pic_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(pic_size)
    i.save(pic_path)
    
    return picture_fname



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender='noreply@demo.com',
                  recipients=[user.email])
    #here i am using _external=True for to create absolute url witch is required for the email
    #and in our application we are using relative urls witch is fine 
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then ignore this email and no changes will be made.
"""
    mail.send(msg)
    