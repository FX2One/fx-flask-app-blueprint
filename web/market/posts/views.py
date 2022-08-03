from flask import render_template, redirect, url_for, flash, request, Blueprint

post_bp = Blueprint('posts', __name__, template_folder='templates')