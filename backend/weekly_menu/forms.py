from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, FloatField, HiddenField
from wtforms.validators import DataRequired

class RegisterWeeklymenuForm(FlaskForm):
    # weekly_id?
    # group_id?

    weekly_name = StringField(
        label=('Navn'),
        validators=[DataRequired()])
    weekly_desc = TextAreaField(
        label=('Beskrivelse'),
        validators=[DataRequired()])

    # recipes = StringField(
    #     label=('Oppskrifter'))

    submit = SubmitField(label=('Registrer ukesmeny'))