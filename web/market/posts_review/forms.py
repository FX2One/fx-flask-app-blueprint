from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class AddReviewForm(FlaskForm):
    review = TextAreaField('Comment the Post', validators=[InputRequired(),
                                                           Length(10, 1000)])

    submit = SubmitField('Submit')


class EditReviewForm(FlaskForm):
    review = TextAreaField('Edit the comment', validators=[InputRequired(),
                                                           Length(10, 1000)])

    submit = SubmitField('Submit')