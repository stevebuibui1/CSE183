from py4web import action, request, abort, redirect, URL
from .common import db, session, T, cache, auth, logger
from .models import get_user_email
import json, os
from .settings import APP_FOLDER
FILE = os.path.join(APP_FOLDER, "data", "table.json")
@action('index')
@action.uses('index.html', auth)
def index():
    f = open(FILE)
    data = json.load(f)
    tophead = ['Bird Species', 'Weight', 'Diet', 'Habitat']
    headers = ['bird', 'weight', 'diet', 'habitat']
    ### You have to modify the code here as well.
    return dict(
        theaders=tophead,
        headers=headers,
        rows=data,
    )
