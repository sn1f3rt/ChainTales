from wtforms import StringField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import Length, InputRequired


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[InputRequired(), Length(min=10, max=100)],
    )
    content = TextAreaField(
        "Content",
        validators=[InputRequired(), Length(min=5, max=1000)],
    )
