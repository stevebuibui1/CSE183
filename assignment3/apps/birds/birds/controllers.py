from py4web import action, request, abort, redirect, URL
from .common import db, session, T, cache, auth, logger
from .models import get_user_email
import json, os
from .settings import APP_FOLDER
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner
import http

url_signer = URLSigner(session)

@action('index') 
@action.uses( 'index.html',url_signer, db, auth.user)
def index():
    rows = db(db.bird.user_email == get_user_email()).select()
    return dict(rows=rows,
                url_signer=url_signer)
    
@action('add', method=["GET", "POST"])
@action.uses("add.html", db, session, auth.user)

def add():
    form = Form(db.bird, csrf_session=session, formstyle=FormStyleBulma)
 
    if form.accepted: 
        redirect(URL('index'))
    

    return dict(form=form)

@action('edit/<bird_id:int>', method=["GET", "POST"])
@action.uses( "edit.html",db, session, auth.user)
def edit(bird_id=None):
    assert bird_id is not None
    birdo = db.bird[bird_id]
    if birdo is None:
       
        redirect(URL('index'))
    form = Form(db.bird, record=birdo, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted: 
        redirect(URL('index'))

    return dict(
        form = form
    )
@action('inc/<bird_id:int>') 
@action.uses(db, session, auth.user, url_signer.verify())

def inc(bird_id=None):
    assert bird_id is not None
    bird = db.bird[bird_id]
    if bird.user_email != get_user_email(): raise http(400)
    db(db.bird.id == bird_id).update(n_sightings=db.bird.n_sightings + 1)
    redirect(URL('index'))
    return dict()

@action('delete/<bird_id:int>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete(bird_id=None):
    assert bird_id is not None
    db(db.bird.id == bird_id).delete()
    redirect(URL('index'))