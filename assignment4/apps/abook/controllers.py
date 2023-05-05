import uuid

from py4web import URL, Field, abort, action, redirect, request
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from .models import get_user_email
from .common import T, auth, cache, db, session, signed_url, logger,flash, Field, authenticated, unauthenticated

url_signer = URLSigner(session)

#hello
@action("index")
#index.html in front so I still have log in
@action.uses("index.html", auth.user, url_signer)
def index():
   # We read all the contact rows as a list (see below).
    rows = db(db.contact.user_email == get_user_email()).select()
    rows = rows.as_list()
   # and then we iterate on each one, to add the phone numbers for the contact.
    for row in rows:
      # empty s string
        s = ""
        #select phone in row
        row_p = db(db.phone.contact_id == row["id"]).select()
        #iterate through the row of phones and append
        for phone in row_p:
            s = s + phone.phone_Number + ' (' + phone.phone_Name + '), '
        #put in dictionary
        row["phone_Numbers"] = s
        
    return dict(
        rows = rows,
        url_signer=url_signer
        
    )

#edit contact
@action('edit/<contact_id:int>', method=["GET", "POST"])
@action.uses('edit.html',db, session, auth.user,  url_signer.verify())
def edit(contact_id = None):
    assert contact_id is not None
    #contact info in model
    p = db.contact[contact_id]
    if p is None:
        redirect(URL('index'))
    #form handler
    form = Form(db.contact, record=p, csrf_session=session, deletable=False, formstyle=FormStyleBulma)

    if form.accepted:
        redirect(URL('index'))

    return dict(form=form,url_signer=url_signer)

#add contact
@action('add', method=["GET", "POST"])
@action.uses('add.html',db, session, auth.user)
def add():
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form = form)

#delete contact
@action('delete/<contact_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user)
def delete(contact_id = None):

    assert contact_id is not None
    if contact_id is None:
            redirect(URL('index'))
    db(db.contact.id == contact_id).delete()
    redirect(URL("index"))

#add phone
@action('add_phones/<contact_id:int>', method=["GET", "POST"])
@action.uses('add_phones.html', auth.user, session)
def add_phone(contact_id = None):
    assert contact_id is not None
    
    phonename = db.contact[contact_id]
    
    if phonename is None:
        redirect(URL('index'))
    
    form = Form([Field('phone_Number'), Field('phone_Name')], csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        db.phone.insert(
            contact_id=contact_id,
            phone_Number=form.vars['phone_Number'],
            phone_Name=form.vars['phone_Name']
        )
        redirect(URL('edit_phones', contact_id, signer=url_signer))
    return dict(name=phonename, form=form)

#edit phone
@action('edit_phones/<contact_id:int>', method=["GET", "POST"])
@action.uses('edit_phones.html',db, auth.user )
def edit_phone(contact_id=None):
    assert contact_id is not None
    #contact info
    contact = db.contact[contact_id]
    print(contact)
    rows = db(db.phone.contact_id ==contact.id).select();
      
    return dict(rows = rows, contact= contact, url_signer= url_signer)
#edit phones
@action('edit_Phone/<contact_id:int>/<phone_id:int>', method=["GET", "POST"])
@action.uses('edit_Phone.html',db, auth.user )
def edit_phones(contact_id=None, phone_id=None):
    assert contact_id is not None
    assert phone_id is not None
    #create contact and phone id
    contact = db.contact[contact_id]
    phone = db.phone[phone_id]
    
    
    if phone is None:
        redirect(URL('edit_phones', contact_id))
    
    #form handler
    form = Form(
        [Field('phone_Number'), Field('phone_Name')],
        record=dict(phone_Number=phone.phone_Number, phone_name=phone.phone_Name), 
        deletable=False,
        csrf_session=session, 
        formstyle=FormStyleBulma
        )
    if form.accepted: 
        db(db.phone.id == phone_id).update(
            contact_id=contact_id,
            phone_Number=form.vars['phone_Number'],
            phone_Name=form.vars['phone_Name'] 
        )
        redirect(URL('edit_phones', contact_id))
        
    return dict(form = form, 
                contact = contact,
                url_signer=url_signer)
    
@action('delete_phone/<contact_id:int>/<phone_id:int>', method=["GET", "POST"])
@action.uses(db, session, auth.user, url_signer.verify())
def delete_phones(contact_id=None, phone_id=None):
    assert contact_id is not None
    assert phone_id is not None
    #delete the phone id
    db(db.phone.id == phone_id).delete()
    redirect(URL('edit_phones', contact_id))