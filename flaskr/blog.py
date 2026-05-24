from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.database import database
from flaskr.models import Post
from werkzeug.exceptions import abort


blueprint = Blueprint('blog', __name__)


@blueprint.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)


@blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            post = Post(
                title=title,
                body=body,
                author_id=g.user.id,
            )
            database.session.add(post)
            database.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = Post.query.filter(Post.id==id).first()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    
    if check_author and post.author != g.user:
        abort(403)
    
    return post


@blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            database.session.add(post)
            database.session.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', post=post)


@blueprint.route('/<int:id>/delete', methods=('POST', ))
@login_required
def delete(id):
    post = get_post(id)
    database.session.delete(post)
    database.session.commit()
    return redirect(url_for('blog.index'))


@blueprint.route('/<int:id>/detail', methods=('GET', ))
def detail(id):
    post = get_post(id, False)
    return render_template('blog/detail.html', post=post)
