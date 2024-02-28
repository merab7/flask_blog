from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort
from flaskblog import  db
from flask_login import current_user, login_required
from flaskblog.posts.forms import (Post_form, Edit_form)
from flaskblog.models import  Post




posts = Blueprint('posts', __name__)



@posts.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    post_form = Post_form()
    if post_form.validate_on_submit():
        new_post = Post(
            title = post_form.title.data,
            content = post_form.content.data,
            author = current_user
        )
        db.session.add(new_post)
        db.session.commit()
        flash(f'{current_user.username}, your post has been created', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='New Post', post_form=post_form)

@posts.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    post_id = request.args.get('id')
    post_to_delete = Post.query.get(post_id)
    if post_to_delete and post_to_delete.author.username == current_user.username:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect(url_for('main.home'))
    else:
        abort(403)

    return redirect(url_for('main.home'))

@posts.route('/post', methods=['GET', 'POST'])
def post():
    post_id = request.args.get('id')
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post )

@posts.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    edit_form = Edit_form()
    post_id = request.args.get('id')
    post = Post.query.get_or_404(post_id)
    if current_user.username == post.author.username:
        if edit_form.validate_on_submit():
            post.title = edit_form.title.data
            post.content = edit_form.content.data 
            db.session.commit()
            flash(f'{current_user.username} your post has been updated', 'success')
            return redirect(url_for('main.home'))   
        else:
            edit_form.title.data = post.title
            edit_form.content.data= post.content 
    else:
        abort(403)        
    return render_template('edit.html', title=post.title, edit_form=edit_form )



