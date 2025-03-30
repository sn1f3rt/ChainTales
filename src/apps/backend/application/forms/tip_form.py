from wtforms import FloatField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired


class TipForm(FlaskForm):
    sender = StringField(
        "Sender",
    )

    recipient = StringField(
        "Recipient",
    )

    amount = FloatField(
        "Amount",
        validators=[InputRequired()],
    )
