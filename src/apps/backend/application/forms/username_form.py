from wtforms import StringField
from flask_wtf import FlaskForm, RecaptchaField
from wtforms.validators import Length, InputRequired


class UsernameForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=10)],
    )
    recaptcha = RecaptchaField()
