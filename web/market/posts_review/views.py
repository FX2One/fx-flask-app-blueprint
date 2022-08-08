from flask import render_template, redirect, url_for, flash, request, Blueprint
from market.posts_review.forms import AddReviewForm, EditReviewForm
from flask_login import current_user, login_required
from market.models import User, Post, Review
from market import db


post_review_bp = Blueprint('posts_review', __name__, template_folder='templates')


@post_review_bp.route('/add_review/<int:post_id>', methods=['GET', 'POST'])
@login_required
def add_review(post_id):
    form = AddReviewForm()
    post = Post.query.filter_by(id=post_id).first_or_404()
    if current_user.is_authenticated:
        if request.method == 'POST':
            if form.validate_on_submit():
                new_review = Review(
                    form.review.data,
                    current_user.id,
                    post_id)
                db.session.add(new_review)
                db.session.commit()
                flash('comment/review added successfully',category="success")
            return redirect(url_for('posts_review.review', post_id=post_id))
    return render_template('add_review.html', form=form)


@post_review_bp.route('/review/<int:post_id>', methods=['GET', 'POST'])
@login_required
def review(post_id):
    users = User.query.all()
    single_post = Post.query.filter_by(id=post_id).first_or_404()
    all_reviews = Review.query.all()
    posts = Post.query.all()
    return render_template('review_posted.html', posts=posts, users=users, single_post=single_post, reviews=all_reviews)



# test_edit_review_form mocking against static user.id
# .env LOGIN_DISABLED=TRUE
# current_user.id exchanged to 1 for test purposes
@post_review_bp.route('/review/edit/<int:post_id>', methods=['GET','POST'])
@login_required
def edit_review(post_id):
    rev = Review.query.filter_by(id=post_id).first_or_404()
    post = Post.query.filter_by(id=rev.post_id).first()
    form = EditReviewForm(request.form, obj=rev)
    if rev.reviewer_id != current_user.id:
        flash('you are not allowed to access this path', category='danger')
        return redirect(url_for('posts.all_owned_posts'))
    if current_user.is_authenticated and rev.reviewer_id == current_user.id:
        if form.validate_on_submit():
            form.populate_obj(rev)
            db.session.commit()
            flash('review edited successfully', category='success')
            return redirect(url_for('posts_review.review', post_id=post.id))
    return render_template('edit_review.html', form=form)


@post_review_bp.route('/delete_review/<int:post_id>', methods=['GET','POST'])
@login_required
def delete_review(post_id):
    rev = Review.query.filter_by(id=post_id).first_or_404()
    post = Post.query.filter_by(id=rev.post_id).first()
    if rev.reviewer_id != current_user.id:
        flash('you are not allowed to access this path', category='danger')
        return redirect(url_for('posts.all_posts'))
    db.session.delete(rev)
    db.session.commit()
    flash('review has been deleted', category='success')
    return redirect(url_for('posts_review.review', post_id=post.id))