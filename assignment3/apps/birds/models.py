"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth, T
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
db.define_table(
    'bird',
    ### TODO: define the fields that are in the json.
    Field('bird', 'string', requires=IS_NOT_EMPTY()),
    Field('weight', 'integer', default=0, requires=IS_NOT_EMPTY()),
    Field('diet', 'string', requires=IS_NOT_EMPTY()),
    Field('habitat', 'string', requires=IS_NOT_EMPTY()),
    Field('n_sightings', 'integer', default=1, requires=IS_NOT_EMPTY()),
    Field('user_email', default=get_user_email)
)
## always commit your models to avoid problems later

db.commit()
