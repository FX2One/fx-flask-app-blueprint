from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, NumberRange

class ItemsForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(),
                                           Length(1, 64)])

    price = IntegerField('Price', validators=[InputRequired(),
                                              NumberRange(min=1, max=9999)])

    barcode = IntegerField('Barcode', validators=[InputRequired(),
                                                  NumberRange(min=1, max=9999999999)])

    description = StringField('Description', validators=[InputRequired(),Length(1,254)])

    submit = SubmitField('Submit')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')