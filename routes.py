from flask import jsonify
from sqlalchemy import func
from main import application, session, Contact, ContactFirstName, ContactLastName, ContactEmail

#Missing routes
@application.route("/<path>", methods=["GET","POST","PATCH","DELETE"])
@application.errorhandler(404)
def home(path=""):
    return jsonify(dict(message="No such path!"))

#List all contacts
@application.route("/", methods=["GET"])
def index():
    return jsonify([x.to_json() for x in session.query(Contact).filter_by(valid_till_date = None).all()])

#Find a contact by username
@application.route("/search/<username>", methods=["GET"])
def search_contact(username=""):
    current_contact = session.query(Contact).filter_by(username=f'{username}', valid_till_date = None).first()
    if current_contact:
        return jsonify(current_contact.to_json())
    else:
        return jsonify(dict(message="No record found!"))

#Create a new contact
@application.route("/create/<username>/<first_name>/<last_name>/<email>", methods=["POST"])
def create_contact(username="",first_name="",last_name="",email=""):
    new_contact = Contact(
        username=username,
        first_name=ContactFirstName(value=first_name),
        last_name=ContactLastName(value=last_name),
        emails=[ContactEmail(value=email)]
    )
    session.add(new_contact)
    session.commit()
    
    return jsonify([x.to_json() for x in session.query(Contact).filter_by(username=f'{username}')])

#Update a contact
@application.route("/update/<username>/<column>/<value>", methods=["PATCH"])
def update_contact(username="", column="",value=""):
    current_contact = session.query(Contact).filter_by(username=f'{username}').first()
    if current_contact:
        if column == "first_name":
            session.query(ContactFirstName).filter_by(contact_id=current_contact.id, valid_till_date = None).first().valid_till_date = func.now()
            session.query(Contact).filter_by(id=current_contact.id).first().first_name = ContactFirstName(value=value)
        elif column == "last_name":
            session.query(ContactLastName).filter_by(contact_id=current_contact.id, valid_till_date = None).first().valid_till_date = func.now()
            session.query(Contact).filter_by(id=current_contact.id).first().last_name = ContactLastName(value=value)
        elif column == "email":
            for e in session.query(ContactEmail).filter_by(contact_id=current_contact.id, valid_till_date = None).all():
                e.valid_till_date = func.now()
            session.query(Contact).filter_by(id=current_contact.id).first().emails = [ContactEmail(value=value)]
    else:
        return jsonify(dict(message="No record found!"))
    
    session.commit()
    
    return jsonify(session.query(Contact).filter_by(username=f'{username}').first().to_json())

#Add new email address to a contact
@application.route("/add_email/<username>/<value>", methods=["POST"])
def add_email(username="",value=""):
    current_contact = session.query(Contact).filter_by(username=f'{username}').first()
    if current_contact:
        current_contact.emails.append(ContactEmail(value=value))
        session.commit()
        return jsonify(session.query(Contact).filter_by(id=current_contact.id).first().to_json())
    else:
        return jsonify(dict(message="Record not found!"))
    
#Delete a contact
@application.route("/delete/<username>", methods=["DELETE"])
def delete_contact(username=""):
    current_contact = session.query(Contact).filter_by(username=f'{username}', valid_till_date = None).first()
    if current_contact:
        current_contact.valid_till_date = func.now()
        session.commit()
        return jsonify(dict(message="Record deleted!"))
    else:
        return jsonify(dict(message="No record found!"))