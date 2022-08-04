from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError
from wtforms.validators import Email, InputRequired, Length, EqualTo
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This user already exists')

    def validate_email_address(self, field):
        if User.query.filter_by(email_address=field.data).first():
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField('Username',validators=[InputRequired()])

    email_address = EmailField('Email', validators=[InputRequired(),
                                                    Length(1, 64),
                                                    Email()])

    password = PasswordField('Password', validators=[InputRequired(),Length(6, max=25)])

    confirm = PasswordField('Repeat Password',validators=[InputRequired(),EqualTo('password')])

    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[InputRequired()])

    password = PasswordField('Password',
                             validators=[InputRequired()])

    submit = SubmitField('Submit')