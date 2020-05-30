from flask import Blueprint
"""This file just brings all of the other files
   in the "api" directory together in a "blueprint"
   and sends them to the app instance.
   
   The rest of the files in this directory define routes for the api.
"""

bp = Blueprint('api', __name__)

from app.api import users, lessons, errors, tokens
