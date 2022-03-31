from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired

class RegisterRecipeForm(FlaskForm):
    dish = StringField(
        label=('Navn på rett'),
        validators=[DataRequired()])
    short_desc = TextAreaField(
        label=('Kort beskrivelse'),
        validators=[DataRequired()])
    long_desc = TextAreaField(
        label=('Lengre beskrivelse - hvordan lager man dette?'),
        validators=[DataRequired()])

    submit = SubmitField(label=('Registrer rett'))
