from flask import render_template, redirect, url_for, flash, request, Blueprint

post_review_bp = Blueprint('posts_review', __name__, template_folder='templates')