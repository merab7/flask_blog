from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request
from flaskblog import  db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from flaskblog.users.forms import (Registration_form, Login_form, Update_account, 
                             RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from sqlalchemy import desc
from flaskblog.users.utils import send_reset_email, save_pic



users = Blueprint('users', __name__)



@users.route("/registration", methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    registration_form = Registration_form()
    if registration_form.validate_on_submit():    
        hashed_password = bcrypt.generate_password_hash(registration_form.password.data).decode('utf-8')
        new_user = User(
            username = registration_form.username.data,
            email = registration_form.email.data,
            password = hashed_password
            )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('main.home')) 

    return render_template("registration.html", title='registration', reg_form=registration_form)



@users.route("/login", methods=['GET', 'POST'])
def login():
# Check if the current user is already authenticated
    if current_user.is_authenticated:
        # If so, redirect them to the home page
        return redirect(url_for('main.home'))

    # Create an instance of the login form
    login_form = Login_form()

    # Validate the form data on submission
    if login_form.validate_on_submit():
        # Query the database for a user with the submitted email
        user = User.query.filter_by(email=login_form.email.data).first()

        # Check if the user exists and the submitted password matches the stored password
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            # If so, log in the user and remember their login status based on the 'remember' checkbox
            login_user(user, remember=login_form.remember.data)

            # Get the next page to redirect to from the request arguments
            next_page = request.args.get('next')

            # Redirect to the next page if it exists, otherwise redirect to the home page
            # This is useful if the user was redirected to the login page from a page that requires login
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            # If the login was unsuccessful, flash a message to the user
            flash('Login unsuccessful. Please check email and password', category='danger')

    # Render the login template
    return render_template("login.html", title="login", log_form=login_form)



@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))




@users.route('/account',  methods=['GET', 'POST'])
@login_required 
def account():
    update_form = Update_account()
    if update_form.validate_on_submit():
        #current_user from flask login gives you this opportunity to get data from database for current user like this
        if update_form.picture.data:
            picture_file = save_pic(update_form.picture.data)
            current_user.image_file = picture_file
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        db.session.commit()
        flash(f'{current_user.username}, your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title="Account", image_file=image_file, update_form = update_form )


@users.route('/authors_posts')
def authors_posts():
   authors_name = request.args.get('author')
   page = request.args.get('page', 1, type=int)
   user = User.query.where(User.username == authors_name).first_or_404()
   posts = Post.query.filter_by(author=user)\
    .order_by(desc(Post.id))\
    .paginate(page=page, per_page=5)
   
   return  render_template('authors_posts.html', posts=posts, user=user)



@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # Check if the current user is already authenticated
    if current_user.is_authenticated:
    # If so, redirect them to the home page
        return redirect(url_for('main.home'))
    reset_request_form = RequestResetForm()   
    if reset_request_form.validate_on_submit():
        user = User.query.filter_by(email=reset_request_form.email.data).first()
        send_reset_email(user)
        flash(f'Reset token has been sent on {user.email}', 'info')
        return redirect(url_for('users.login'))
    return  render_template('reset_request.html', title='Reset Password', form=reset_request_form) 



@users.route('/reset_token', methods=['GET', 'POST'])
def reset_token():
    token = request.args.get('token')
    # Check if the current user is already authenticated
    if current_user.is_authenticated:
    # If so, redirect them to the home page
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token=token)
    if not user :
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    reset_password_form = ResetPasswordForm()
    if reset_password_form.validate_on_submit():  
        hashed_password = bcrypt.generate_password_hash(reset_password_form.password.data).decode('utf-8')
        user.password =  hashed_password
        db.session.commit()
        flash(f'Your password has been updated!', 'success')
        return redirect(url_for('users.login')) 
    return  render_template('reset_token.html', title='Reset Password', form=reset_password_form) 



@users.route('/my-posts')
def my_posts():
   page = request.args.get('page', 1, type=int)
   user = User.query.where(User.username == current_user.username).first_or_404()
   posts = Post.query.filter_by(author=user)\
    .order_by(desc(Post.id))\
    .paginate(page=page, per_page=5)
   
   return  render_template('my_posts.html', posts=posts, user=user)

