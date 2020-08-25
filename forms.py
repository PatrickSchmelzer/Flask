import flask_wtf
import wtforms
import wtforms.validators

class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', validators=[wtforms.validatorsDataRequired()])
    password = wtforms.PasswordField('Password', validators=[wtforms.validatorsDataRequired()])
    remember_me = wtforms.BooleanField('Remember Me')
    submit = wtforms.SubmitField('Sign In')
