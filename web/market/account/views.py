from flask import render_template, redirect, url_for, flash, request, Blueprint

account_bp = Blueprint('account', __name__, template_folder='templates')

@account_bp.route('/')
@account_bp.route('/home')
def home_page():
    return render_template('home.html')


