"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField

class AddPetForm(FlaskForm):
    """Form to add a pet"""

    name = StringField("Name")
    species = StringField("Species")
    photo_url = StringField("Photo URL")
    age = SelectField("Age",
        choices=[("baby", "Baby"),
                ("young", "Young"),
                ("adult", "Adult"),
                ("senior", "Senior")])
    notes = StringField("Notes")
    available = RadioField("Available",
        choices=[("true", "True"), ("false", "False")],
        coerce=bool)