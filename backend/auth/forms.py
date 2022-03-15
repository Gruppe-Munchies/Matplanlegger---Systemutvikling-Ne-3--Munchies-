from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField(
        label=('Brukernavn'),
        validators=[DataRequired(),
                    Length(min=5,
                           max=24,
                           message='Brukernavnet må være mellom 5 og 24 tegn')])

    lastname = StringField(
        label=('Etternavn'),
        validators=[DataRequired()])

    firstname = StringField(
        label=('Fornavn'),
        validators=[DataRequired()])

    email = StringField(
        label=('Epost'),
        validators=[
            DataRequired(),
            Email(message="Vennligst oppgi en gyldig epostadresse")])

    password = PasswordField(
        label=('Passord'),
        validators=[DataRequired(),
                    Length(min=8,
                           message='Passordet må være minst 8 tegn langt')])

    confirm = PasswordField(
        label=('Gjenta passord'),
        validators=[DataRequired(message='*Required'),
                    EqualTo('password',
                            message='Passordene må være like')])

    usergroup = SelectField('Brukergruppe',
        choices=[('MatMons'), ('Familien Hansen')], # Må kjøre en query fra usergroup for å hente verdier her
        validate_choice=True)



    usertype = SelectField('Brukertype',
        choices=[('1', 'Admin'), ('2', 'Bruker')],# Må kjøre en query fra usertype for å hente verdier her
        validate_choice=True)

    submit = SubmitField(label=('Registrer'))


class InviteForm(FlaskForm):
    username = StringField(
        label=('Brukernavn'),
        validators=[DataRequired()])

    usergroup = SelectField(
        label=('Brukergruppe'),
        validators=[DataRequired()])

    usertype = SelectField(
        label=('Brukertype'),
        validators=[DataRequired()])

    submit = SubmitField(label=('Inviter'))


class createUserGroupForm(FlaskForm):
    usergroup = StringField(
        label=('Brukergruppe'),
        validators=[DataRequired()])

    submit = SubmitField(label=('Opprett gruppe'))