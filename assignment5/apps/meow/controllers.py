
import datetime
import random

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.url_signer import URLSigner
from .models import get_username, get_user_email

# Some constants.
MAX_RETURNED_USERS = 20 # Our searches do not return more than 20 users.
MAX_RESULTS = 20 # Maximum number of returned meows. 
url_signer = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth.user,url_signer)
def index():
    # lists all posts filtered by followed
    

    return dict(
        get_my_users= URL('get_users', signer=url_signer),
        followed= URL('set_follow', signer=url_signer),
        cur_user = URL('get_current_user', signer=url_signer),
        added_post =URL('add_post', signer=url_signer),
    )

@action("get_users")
@action.uses(db, auth.user)
def get_users():
    current_user = auth.current_user.get('username')  # Get the username of the current user
    #if if the user in the list is not the current user, then select
    users = db(db.auth_user.username != current_user).select(db.auth_user.username).as_list()
    
    return dict(users=users)


@action("set_follow", method="POST")
@action.uses(db, auth.user)
def set_follow():
    # Implement.
    
    return "ok"

@action("get_current_user")
@action.uses(db, auth.user)
def get_current_user():
    current_user = get_username();
    
    return dict(cur_user= current_user)

@action('add_post', method="POST")
@action.uses(db,auth.user,url_signer.verify())
def add_post():
    name = get_username();
    email= get_user_email();
    print(name)
    print(email)
    
    id = db.post.insert(
        post_text = request.json.get('post_text'),
        username = name,
        
        )
    return dict(postid= id,
                username = name,
                email = email)