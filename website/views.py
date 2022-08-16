# it will contains all routed related to core blog application like home page ,users profile

from flask import Blueprint,render_template , request , flash , redirect, url_for
from flask_login import login_required , current_user
from .models import Post,User
from . import db


# blueprint for storing diff routes
views2 = Blueprint("views",__name__) # views -> name of our blueprint


@views2.route("/")
@views2.route("/home")
@login_required
def home():
    posts = Post.query.all() 
    return render_template("home.html",name=current_user.username,user=current_user,posts=posts) # name is variable in html and defined in backend as sunil , we can pass info from our backend to our frontend with render_template

@views2.route("/create-post",methods=["GET","POST"])
@login_required # you can not make a post unless you are logged in
def create_post():
    if request.method == "POST":
        text = request.form.get("text") 

        if not text:
            flash("Post canbot be empty",category="error")
        else:
            post = Post(text=text , author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created! ",category="success")
            return redirect(url_for("views.home"))

    return render_template("create_post.html",user=current_user)

@views2.route("/delete-post/<id>")
@login_required
def delete_post(id):

    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist." , category="error")
    elif current_user.id != post.id :
        flash("you do not have permission to delete this post.",category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("post deleted.",category="success")
    return redirect(url_for("views.home"))

@views2.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User does not exist with this username",category="error")
        return redirect(url_for("views.home"))

    posts = user.posts

    return render_template("posts.html",user=current_user , posts=posts, username=username)


