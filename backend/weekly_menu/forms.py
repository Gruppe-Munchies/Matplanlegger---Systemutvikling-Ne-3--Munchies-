from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, FloatField, HiddenField
from wtforms.validators import DataRequired, ValidationError, NumberRange, InputRequired


class RegisterWeeklymenuForm(FlaskForm):
    weekly_name = StringField(
        label=('Navn'),
        validators=[DataRequired()])
    weekly_desc = TextAreaField(
        label=('Beskrivelse'),
        validators=[DataRequired()])

    submit = SubmitField(label=('Registrer ukesmeny'))


class WeeklyMenuSelector(FlaskForm):
    weeklyIdName = SelectField(u'Group', choices='', validators=[DataRequired()])


class WeeklyMenuToDateForm(FlaskForm):
    week = IntegerField("Uke", validators=[DataRequired(), NumberRange(1, 52)])
    year = IntegerField("År", validators=[DataRequired(), NumberRange(0, 2100)])
    submit = SubmitField(label=('Knytt meny til uke'))
