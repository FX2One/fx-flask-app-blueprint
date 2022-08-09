from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(10, 60)])

    post = TextAreaField('Post Section', validators=[InputRequired(),
                                                     Length(10, 2000)])

    submit = SubmitField('Submit')


class EditPostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(10, 60)])

    post = TextAreaField('Post Section', validators=[InputRequired(),
                                                     Length(10, 2000)])

    submit = SubmitField('Submit')
