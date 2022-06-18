"""Flask app for adopt app."""

from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
import random
import requests
import os

app = Flask(__name__)

SECRET_KEY = os.environ['PETFINDER_SECRET_KEY']
PETFINDER_API_KEY = os.environ['PETFINDER_API_KEY']
# auth_token = os.environ['PET_FINDER_ACCESS_TOKEN']
app.config['SECRET_KEY'] = "SECRET!"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
auth_token = None

@app.before_first_request
def refresh_credentials():
    """Get auth_token"""

    global auth_token
    auth_token = update_auth_token_string()

"""Need to verify/check. Currently getting "Access token invalid or expired"""
def update_auth_token_string():
    """Update auth_token"""
    

    resp = requests.post(
        "https://api.petfinder.com/v2/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": PETFINDER_API_KEY,
            "client_secret": SECRET_KEY,
        })

    

    response = resp.json()    

    return response['access_token']

# TODO: this function should be the one that returns a single pet, currently
# functionality is in display_home()
# def display_list_pets():

#     resp = requests.get(
#         "https://api.petfinder.com/v2/animals",
#         headers={"Authorization": f"Bearer {auth_token}"},
#         params={"limit": 100},
#     )

#     pet_index = random.randrange(0,99)
#     animal = resp.data.animals[pet_index]
#     print(animal)



@app.get("/")
def display_home():
    """Display homepage with pets"""

    #TODO: move this into it's own function - separation of concerns
    resp = requests.get(
        "https://api.petfinder.com/v2/animals",
        headers={"Authorization": f"Bearer {auth_token}"},
        params={"limit": 100},
    )

    animal_data = resp.json()

    pet_index = random.randrange(0,99)
    animal = animal_data['animals'][pet_index]
    
    new_pet = Pet(
            name=animal['name'],
            species=animal['species'],
            photo_url= animal['primary_photo_cropped']['medium'] if animal['primary_photo_cropped'] else '',
            age=animal['age'],
        )

    db.session.add(new_pet)
    db.session.commit()

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
