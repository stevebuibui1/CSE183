"""
This file defines the database models
"""

import datetime
import random
from py4web.utils.populate import FIRST_NAMES, LAST_NAMES, IUP
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_username():
    return auth.current_user.get('username') if auth.current_user else None


def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
db.define_table('post',
                Field('username', default=get_username),
                Field('email',default=get_user_email),
                Field('time', default= get_time),
                Field('post_text', requires=IS_NOT_EMPTY())
                )
# db.define_table('follow',
#                 Field('user_id', 'reference auth_user'),
#                 Field('following', 'boolean', default=False)
#                 )
## always commit your models to avoid problems later

db.commit()

def add_users_for_testing(num_users):
    # Test user names begin with "_".
    # Counts how many users we need to add.
    db(db.meow).delete()
    db(db.follow).delete()
    db(db.auth_user.username.startswith("_")).delete()
    num_test_users = db(db.auth_user.username.startswith("_")).count()
    num_new_users = num_users - num_test_users
    print("Adding", num_new_users, "users.")
    for k in range(num_test_users, num_users):
        first_name = random.choice(FIRST_NAMES)
        last_name = first_name = random.choice(LAST_NAMES)
        username = "_%s%.2i" % (first_name.lower(), k)
        user = dict(
            username=username,
            email=username + "@ucsc.edu",
            first_name=first_name,
            last_name=last_name,
            password=username,  # To facilitate testing.
        )
        auth.register(user, send=False)
        # Adds some content for each user.
        ts = datetime.datetime.utcnow()
        for n in range(3):
            ts -= datetime.timedelta(seconds=random.uniform(60, 1000))
            m = dict(
            author=username,
            timestamp = ts,
            content=" ".join(random.choices(list(IUP.keys()), k=20))
            )
            db.meow.insert(**m)
    db.commit()
    
# Comment out this line if you are not interested. 
add_users_for_testing(5)
