from typing import Any, Callable

from wtforms import StringField
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Length, InputRequired, ValidationError


class KYCForm(FlaskForm):
    @staticmethod
    def file_size_limit(max_size: int) -> Callable:
        def _file_size_limit(_: Any, field: FileField) -> None:
            if field.data and len(field.data.read()) > max_size:
                raise ValidationError(
                    f"File size must be less than {max_size / (1024 * 1024)} MB."
                )
            field.data.seek(0)

        return _file_size_limit

    name = StringField(
        "Name",
        validators=[InputRequired(), Length(min=5, max=100)],
    )
    age = StringField(
        "Age",
        validators=[InputRequired(), Length(min=1, max=3)],
    )
    location = StringField(
        "Location",
        validators=[InputRequired(), Length(min=5, max=100)],
    )
    id_number = StringField(
        "ID Number",
        validators=[InputRequired(), Length(min=5, max=20)],
    )
    id_front = FileField(
        "ID Card Front",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png"], "Images only!"),
            file_size_limit(1 * 1024 * 1024),
        ],
    )
    id_back = FileField(
        "ID Card Back",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png"], "Images only!"),
            file_size_limit(1 * 1024 * 1024),
        ],
    )
    recaptcha = RecaptchaField()
