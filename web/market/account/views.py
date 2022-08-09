from flask import render_template, redirect, url_for, flash, Blueprint
from market.account.forms import RegisterForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from market.models import User, Item
from market import db
from ..email import send_email

account_bp = Blueprint('account', __name__, template_folder='templates')


@account_bp.route('/')
@account_bp.route('/home')
def home_page():
    return render_template('home.html')


@account_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password.data)
        db.session.add(create_user)
        db.session.commit()
        login_user(create_user)
        token = create_user.generate_auth_token()
        confirm_link = url_for('account.confirm', token=token, _external=True)
        send_email(create_user.email_address, 'Confirm your account', 'confirm', user=create_user, token=token,
                   confirm_link=confirm_link)
        flash('You are now registered and successfully logged in', category='success')
        flash('confirmation email has been sent', category='success')
        return redirect(url_for('items.market_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@account_bp.route('/email/confirm/<token>', methods=['GET', 'POST'])
def confirm(token):
    if current_user.is_authenticated:
        """Confirm new user's account with provided token."""
        if current_user.email_confirmed:
            return redirect(url_for('items.market_page'))
        if current_user.confirm(token):
            flash('Your account has been confirmed.', category='success')
        else:
            flash('The confirmation link is invalid or has expired.',
                  category='danger')
        return redirect(url_for('items.market_page'))
    else:
        flash('Please login first to activate your account', category='danger')
        return redirect(url_for('account.login_page'))


@account_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(plain_password=form.password.data):
            login_user(user)
            flash('you are successfully logged in', category='success')
            return redirect(url_for('account.home_page'))
        else:
            flash('user or password do not match', category='danger')
    return render_template('login.html', form=form)


@account_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout_page():
    logout_user()
    flash('you have been logged out', category='info')
    return redirect(url_for('account.home_page'))
