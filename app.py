"""Flask app for adopt app."""

from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
import os

app = Flask(__name__)

SECRET_KEY = os.environ['PETFINDER_SECRET_KEY']
PETFINDER_API_KEY = os.environ['PETFINDER_API_KEY']
ACCESS_TOKEN = os.environ['PETFINDER_ACCESS_TOKEN']

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

@app.before_first_request
def refresh_credentials():
    """Get auth_token"""

    global auth_token
    auth_token = update_auth_token_string()


@app.get("/")
def display_home():
    """Display homepage with pets"""

    pets = Pet.query.all()
    return render_template("home.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def display_add_pet_form():
    """Display add pet form and add pet upon submittal of valid data
        If pet info is invalid, reloads add_pet form
        If pet info is valid, loads homepage and flashes message confirming
        pet was added"""

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = True if form.available.data == 'True' else False

        pet = Pet(
            name=name,
            species=species,
            photo_url=photo_url,
            age=age,
            notes=notes,
            available=available,
        )

        db.session.add(pet)
        db.session.commit()

        flash(f"Added {name}!")
        return redirect("/")
    else:
        return render_template("add_pet.html", form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def display_or_edit_pet(pet_id):
    """Display pet info and edit pet form
    and update pet info upon submittal of valid data
    The edit pet form only allows edit of photo_url, notes, and available
    
    If valid fields, redirects back to pet info page and confirms update
    If invalid fields, reloads pet info template"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    breakpoint()

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = True if form.available.data == 'True' else False

        db.session.commit()

        flash(f"Updated {pet.name}!")
        return redirect(f"/{pet_id}")
    else:
        return render_template("pet_info.html", form=form, pet=pet)
