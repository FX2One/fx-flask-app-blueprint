from flask import render_template, redirect, url_for, flash, request, Blueprint
from market.notes.forms import NoteForm, EditNoteForm
from flask_login import current_user, login_user, logout_user, login_required
from market.models import User, Note
from market import db

note_bp = Blueprint('notes', __name__, template_folder='templates')


@note_bp.route('/add_note', methods=['GET', 'POST'])
@login_required
def add_note():
    form = NoteForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_note = Note(
            form.title.data,
            form.notation.data,
            current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('item has been added successfully!', category="success")
        return redirect(url_for('notes.all_owned_notes'))
    return render_template('add_note.html', form=form)


@note_bp.route('/all_owned_notes', methods=['GET', 'POST'])
@login_required
def all_owned_notes():
    all_user_notes = Note.query.filter_by(notation_id=current_user.id)
    return render_template('all_owned_notes.html', notes=all_user_notes)


@note_bp.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(id=note_id).first_or_404()
    form = EditNoteForm(request.form, obj=note)
    if note.notation_id != current_user.id:
        flash('you are not allowed to edit this item', category='danger')
        return redirect(url_for('account.home_page'))
    if current_user.is_authenticated and note.notation_id == current_user.id:
        if form.validate_on_submit():
            form.populate_obj(note)
            db.session.commit()
            flash('you successfully edited this item', category='success')
            return redirect(url_for('notes.all_owned_notes'))
    return render_template('edit_note.html', form=form)


@note_bp.route('/delete_note/<int:note_id>', methods=['GET','POST'])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id).first_or_404()
    if note.notation_id != current_user.id:
        flash('you are not allowed to access this path', category='danger')
        return redirect(url_for('notes.all_owned_notes'))
    db.session.delete(note)
    db.session.commit()
    flash('note has been deleted', category='success')
    return redirect(url_for('notes.all_owned_notes'))