from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class NoteForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),Length(10, 60)])

    notation = StringField('Note', validators=[InputRequired(),
                                               Length(10, 999)])

    submit = SubmitField('Submit')


class EditNoteForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(),Length(10, 60)])

    notation = StringField('Note', validators=[InputRequired(),
                                               Length(10, 999)])

    submit = SubmitField('Submit')