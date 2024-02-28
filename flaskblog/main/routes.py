from flask import Blueprint, render_template, request
from flaskblog.models import Post
from sqlalchemy import desc




main = Blueprint('main', __name__)





@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(desc(Post.id)).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)



