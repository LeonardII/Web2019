from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from dataModels import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=50)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        user = User.query.filter_by(Name=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(Email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Angemeldet bleiben')
    submit = SubmitField('Anmelden')

class SuggestQuestionForm(FlaskForm):
    question = StringField('Frage',validators=[DataRequired(),Length(min=2,max=200)])
    right_answer = StringField('Richtige Antwort',validators=[DataRequired(), Length(min=2,max=200)])
    false_answer_1 = StringField('Falsche Antwort 1',validators=[DataRequired(), Length(min=2,max=200)])
    false_answer_2 = StringField('Falsche Antwort 2',validators=[DataRequired(), Length(min=2,max=200)])
    false_answer_3 = StringField('Falsche Antwort 3',validators=[DataRequired(), Length(min=2,max=200)])
    submit = SubmitField('Frage hinzufügen')


class ScoreSubmitForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    submit = SubmitField('Submit')

class AnswerQuestionForm(FlaskForm):
    option_eins = SubmitField('A')
    option_zwei = SubmitField('B')
    option_drei = SubmitField('C')
    option_vier = SubmitField('D')