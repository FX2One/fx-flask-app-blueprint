from flask import render_template, redirect, url_for, flash, request, Blueprint
from market.posts.forms import AddPostForm, EditPostForm
from flask_login import current_user, login_required
from market.models import User, Post
from market import db

post_bp = Blueprint('posts', __name__, template_folder='templates')


@post_bp.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_post = Post(
            form.title.data,
            form.post.data,
            current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash(
            f"new post {new_post.title} has been added successfully!", category="success")
        return redirect(url_for('posts.all_owned_posts'))
    return render_template('add_post.html', form=form)


@post_bp.route('/all_posts', methods=['GET', 'POST'])
def all_posts():
    all_users = User.query.all()
    all_user_posts = Post.query.all()
    return render_template('all_posts.html', posts=all_user_posts, users=all_users)


@post_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def single_post(post_id):
    single_post = Post.query.filter_by(id=post_id).first_or_404()
    posts = Post.query.all()
    users = User.query.all()
    return render_template('single_post.html', single_post=single_post, posts=posts, users=users)


@post_bp.route('/all_owned_posts', methods=['GET', 'POST'])
@login_required
def all_owned_posts():
    all_users = User.query.all()
    all_user_posts = Post.query.filter_by(author_id=current_user.id)
    return render_template('all_owned_posts.html', posts=all_user_posts, users=all_users)


# test_edit_post_form mocking against static user.id
# .env LOGIN_DISABLED=TRUE
# current_user.id exchanged to 1 for test purposes
@post_bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = EditPostForm(request.form, obj=post)
    if post.author_id != current_user.id:
        flash('you are not allowed to access this path', category='danger')
        return redirect(url_for('posts.all_owned_posts'))
    if current_user.is_authenticated and post.author_id == current_user.id:
        if form.validate_on_submit():
            form.populate_obj(post)
            db.session.commit()
            return redirect(url_for('posts.single_post', post_id=post.id))
    return render_template('edit_post.html', form=form)


@post_bp.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if post.author_id != current_user.id:
        flash('you are not allowed to access this path', category='danger')
        return redirect(url_for('posts.all_posts'))
    db.session.delete(post)
    db.session.commit()
    flash('post has been deleted', category='success')
    return redirect(url_for('posts.all_owned_posts'))
