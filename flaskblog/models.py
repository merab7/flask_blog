from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin  # usermixin is class that contains isouthenticated is_active isanonymus ...
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app



#user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#USER MODEL
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250),unique=True, nullable=False)
    image_file: Mapped[str] = mapped_column(String(20), nullable=False, default='default.jpg')
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    #i am declaring post attribute and saying that is has relation to 
    #Post table model and it should be in quotes '' and 
    #backref is the same as creating column so here i am creating
    #author column and in this column will be the author of the post
    #lazy argument says when tha sqlalchemy loads the data, and setting it true means
    #load the date as necessary at one go
    post = relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod#this decorator says to python to not to expect 'self'
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)    


    def __repr__(self) -> str:
        return f"User('{self.username}','{self.email}','{self.image_file}')"
    
#Post Model
class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    #with utc time i do not use a () because i want it to be
    #a argument and in databases you should always use utc time#
    # for it to be consistent
    date_posted: Mapped[str] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    #here user in Foreign ket is lower case despite the fact that User table is upper case and 
    #also Post in post attribute  was upper case adn that because it refers to specific user in  Users class
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=True)


    def __repr__(self) -> str:
        return f"Post('{self.title}','{self.date_posted}')"
    

    #creating tables

    
