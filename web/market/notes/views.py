from flask import render_template, redirect, url_for, flash, request, Blueprint

note_bp = Blueprint('notes', __name__, template_folder='templates')