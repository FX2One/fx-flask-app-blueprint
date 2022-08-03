from flask import render_template, redirect, url_for, flash, request, Blueprint

account_bp = Blueprint('account', __name__, template_folder='templates')