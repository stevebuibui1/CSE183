"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import uuid
from yatl.helpers import A, SPAN
from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from .common import db, Field, auth, T
from pydal.validators import *
from .models import get_user_email
from . common import db, session, T, cache, auth, signed_url

url_signer = URLSigner(session)

@action('index')
@action.uses('index.html',url_signer, db, auth.user)
def index():
    print("serving hw4 !")
    rows = db(
        db.contact.user_email == get_user_email()
    ).select().as_list()

    allNums ={}
    prettyString=""
    for r in rows:
        allNums = db(
                 (db.phone.contact_id == r['id'])
                 ).select().as_list()

        for num in allNums:
            prettyString += (num["phone_number"] + "(" + num["phone_name"]+ ")" + ", ")
        print(prettyString)
        r["phone_numbers"] = prettyString 
        prettyString=""





    return dict(rows=rows, url_signer=url_signer, ) # USER VALIDATE



@action('add', method=["GET", "POST"])
@action.uses('add.html', db, session, auth.user, url_signer)
def add():
 
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form=form)



@action('delete/<product_id:int>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete(product_id=None):
    assert product_id is not None
    db(db.contact.id == product_id).delete()
    redirect(URL('index'))




@action('delete_phone/<product_id:int>/<phone_id:int>')
@action.uses(db, session, auth.user, url_signer.verify())
def delete(product_id=None ,phone_id=None):
    assert product_id is not None
    assert phone_id is not None

    p = db(
        (db.phone.contact_id == db.contact.id) &
        (db.phone.id == phone_id)
    ).select().first()


    db(db.phone.id == phone_id).delete()
    redirect(URL('edit_phones', product_id, signer=url_signer))


@action('edit/<product_id:int>', method=["GET", "POST"])
@action.uses('edit.html', url_signer.verify(), db, session, auth.user)
def edit(product_id=None):
    assert product_id is not None
    p = db.contact[product_id]
    if p is None:
        redirect(URL('index'))
    # THIS IS AN EDIT FORM--> Use the record
    form = Form(db.contact, record=p, deletable=False, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # The update already happened!
        redirect(URL('index'))
    return dict(form=form) # if error/empty, just return the form again




#THIS IS AN EDIT FORM --> USE THE RECORD
@action('edit_phones/<product_id:int>')
@action.uses('edit_phones.html', url_signer.verify(), db, session, auth.user)
def edit_phones(product_id=None):
    print("heeey")

    firstName = db.contact[product_id].first_name
    lastName = db.contact[product_id].last_name
    currID =product_id



    rows = db(
            (db.contact.first_name == firstName)&
            (db.contact.last_name == lastName)&
            (db.phone.contact_id == db.contact.id)

        ).select()

    rows2 = db(
            (db.contact.first_name == firstName)&
            (db.contact.last_name == lastName)

        ).select()

    for row in rows:
        print(row)
    # print(p)
    # for r in rows:
    #     print("hey")
    #     print(r.contact.user_email)

    return dict(rows=rows, currContact = firstName +" " + lastName, currID=currID, url_signer=url_signer)


#return rows of contacts



#GET will get the empty form
#POST will post infromation back to database
@action('add_phone/<product_id:int>', method=["GET", "POST"])
@action.uses('add_phone.html', db, session, auth.user, url_signer)
def add(product_id=None):
    assert product_id is not None
    print("serving add phone")
    form = Form([Field('phone', requires=IS_NOT_EMPTY()), Field('kind', requires=IS_NOT_EMPTY())], csrf_session=session,
                formstyle=FormStyleBulma)
    form.param.sidecar.append(SPAN(" ", A('Cancel', _class="button is-danger", _href=URL('index'))))

    if form.accepted:
        db.phone.insert(
            contact_id = product_id,
            phone_number=form.vars["phone"],
            phone_name=form.vars["kind"]
        )

        # if the form is accepted, redirect back to the Index, where user's birds are displayed
        redirect(URL('edit_phones', product_id, signer=url_signer))
    return dict(form=form)



#GET will get the empty form
#POST will post infromation back to database
@action('edit_phone/<product_id:int>/<phone_id:int>', method=["GET", "POST"])
@action.uses('edit_phone.html', db, session, auth.user, url_signer)
def add(product_id=None, phone_id= None):
    assert product_id is not None
    assert phone_id is not None
    #declaring a form & how it is to be constructed
    # THIS IS AN INSERT FORM, NO PREV RECORD
    print("serivng edit phone")

    phoneNum = db.phone[phone_id].phone_number
    phoneName = db.phone[phone_id].phone_name

    lastName = db.contact[product_id].last_name
    firstName = db.contact[product_id].last_name



    p = db(
        (db.phone.contact_id == db.contact.id)&
        (db.phone.id == phone_id)
    ).select().first()

    print(phoneNum)
    print(phoneName)
    print(p)


    form = Form([Field('phone'), Field('kind')],
                record=dict(phone=p.phone.phone_number, kind=p.phone.phone_name),
                csrf_session=session,
                formstyle=FormStyleBulma)
    form.param.sidecar.append(SPAN(" ", A('Cancel', _class="button", _href=URL('index'))))

    if form.accepted:
        p.phone.phone_number = form.vars["phone"]
        p.phone.phone_name= form.vars["kind"]
        p.phone.update_record()


        # if the form is accepted, redirect back to the Index, where user's birds are displayed
        redirect(URL('edit_phones', product_id, signer=url_signer))
    return dict(form=form)