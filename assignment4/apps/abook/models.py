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
#
## always commit your models to avoid problems later

db.define_table(
    'contact',
    Field('first_name',default="", requires=IS_NOT_EMPTY()),
    Field('last_name',default="", requires=IS_NOT_EMPTY()),
    Field('user_email', default=get_user_email),
)


db.define_table(
    'phone',
    Field('contact_id', 'reference contact', ondelete="CASCADE"),
    Field('phone_number', default="",requires=IS_NOT_EMPTY()),
    Field('phone_name', default="",requires=IS_NOT_EMPTY()),
)



db.contact.first_name.label = T(" First Name ")
db.contact.last_name.label = T(" Last Name ")




db.contact.id.readable = db.contact.id.writable = False
db.contact.user_email.readable = db.contact.user_email.writable  = False


db.commit()
