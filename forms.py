"""Forms for adopt app."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField
from wtforms.validators import InputRequired, Optional, URL, AnyOf


class AddPetForm(FlaskForm):
    """Form to add a pet"""

    name = StringField("Name",
                       validators=[InputRequired()])
    species = StringField("Species",
                          validators=[InputRequired(),
                                      AnyOf(['cat', 'dog', 'porcupine', 'panda'])])
    photo_url = StringField("Photo URL",
                            validators=[Optional(), URL()])
    age = SelectField("Age",
                      choices=[("baby", "Baby"),
                               ("young", "Young"),
                               ("adult", "Adult"),
                               ("senior", "Senior")],
                      validators=[InputRequired()])
    notes = StringField("Notes")
    available = RadioField("Available",
                           choices=[("true", "True"), ("false", "False")],
                           coerce=bool,
                           validators=[InputRequired()])


class EditPetForm(FlaskForm):
    """Form to edit a pet's info"""

    photo_url = StringField("Photo URL",
                            validators=[Optional(), URL()])
    notes = StringField("Notes")
    available = RadioField("Available",
                           choices=[("true", "True"), ("false", "False")],
                           coerce=bool,
                           validators=[InputRequired()])
