from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class RegisterRecipeForm(FlaskForm):
    dish = StringField(
        label=('Navn på rett'),
        validators=[DataRequired()])
    short_desc = StringField(
        label=('Kort beskrivelse'),
        validators=[DataRequired()])
    long_desc = StringField(
        label=('Lengre beskrivelse - hvordan lager man dette?'),
        validators=[DataRequired()])


    submit = SubmitField(label=('Registrer rett'))