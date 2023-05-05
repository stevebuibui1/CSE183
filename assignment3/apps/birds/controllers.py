from py4web import action, request, abort, redirect, URL, Field
from .common import db, session, cache, auth, logger
from .models import get_user_email
import json
import os
from .settings import APP_FOLDER
from py4web.utils.url_signer import URLSigner
from py4web.utils.form import Form, FormStyleBulma
urlSigner = URLSigner(session)

@action('index')
@action.uses('index.html', db, auth, urlSigner)
def index():
    ### You have to modify the code here as well.
    info = db(db.bird.user_email == get_user_email()).select()
    return dict(info = info, urlSigner = urlSigner)

@action('add', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'add.html')
def add():
    form = Form(db.bird, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form = form)


@action('edit/<bird_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, 'edit.html', urlSigner.verify())
def edit(bird_id):
    assert bird_id is not None

    if bird_id is None:
        redirect(URL('index'))

    bird_id = int(bird_id)

    bird_record = db.bird[bird_id]
    form = Form(db.bird, record=bird_record, csrf_session=session, formstyle=FormStyleBulma)

    if bird_record is None:
        redirect(URL('index'))
        
    if form.accepted:
        redirect(URL('index'))

    return dict(form=form)


@action('inc/<bird_id:int>')
@action.uses(db, auth.user, session)
def inc(bird_id):
    assert bird_id is not None
    if bird_id is None:
        redirect(URL('index'))
    bird = db.bird[bird_id]
    db(db.bird.id == bird_id).update(n_sightings=(int(bird.n_sightings) + 1))
    redirect(URL('index'))
    return dict()

@action('del/<bird_id:int>')
@action.uses(db, session, auth.user)
def delete(bird_id):
    assert bird_id is not None
    if bird_id is None:
        redirect(URL('index'))
    bird_id = int(bird_id)
    db(db.bird.id == bird_id).delete()
    redirect(URL('index'))
