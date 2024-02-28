import os

class Config:
    SECRET_KEY = os.environ.get('BLOG_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('BLOG_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MY_EMAIL')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')