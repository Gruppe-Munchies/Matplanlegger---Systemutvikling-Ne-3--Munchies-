from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    ingredientName = StringField(
        label=('Navn på ingrediens'),
        validators=[DataRequired()])

    price = StringField(
        label=('Pris per enhet'),
        validators=[DataRequired()])

    unit = StringField(
        label=('Enhet'),
        validators=[DataRequired()])

    submit = SubmitField(label=('Registrer ingrediens'))
