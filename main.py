from flask import Flask
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine, MetaData, func, ForeignKey, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from celery_worker import make_celery
from celery.task.base import periodic_task
from random import choice
from string import ascii_uppercase
from time import sleep
from datetime import timedelta

application = Flask(__name__)
application.config['JSON_SORT_KEYS'] = False
application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'

engine = create_engine(r'sqlite:///contact_management_model.db', connect_args={'check_same_thread': False})
metadata = MetaData(engine)
Base = declarative_base(application)
Session = sessionmaker(bind=engine)
session = Session()
celery = make_celery(application)

class Contact(Base):
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    insert_date = Column(DateTime(), server_default=func.now())
    valid_till_date = Column(DateTime(), nullable=True)
    
    first_name = relationship("ContactFirstName", uselist=False,
                     cascade="all, delete, delete-orphan", primaryjoin="and_(Contact.id==ContactFirstName.contact_id, "
                        "ContactFirstName.valid_till_date == None)")
    
    last_name = relationship("ContactLastName", uselist=False, 
                     cascade="all, delete, delete-orphan", primaryjoin="and_(Contact.id==ContactLastName.contact_id, "
                        "ContactLastName.valid_till_date == None)")
    
    emails = relationship("ContactEmail", back_populates='contact',
                     cascade="all, delete, delete-orphan", primaryjoin="and_(Contact.id==ContactEmail.contact_id, "
                        "ContactEmail.valid_till_date == None)")
        
    def to_json(self):
        return dict(username=self.username, first_name=self.first_name.value, last_name=self.last_name.value, emails=[x.value for x in self.emails], insert_date=self.insert_date, valid_till_date=self.valid_till_date)
    
    def __repr__(self):
        return "<User(username='%s', first_name='%s', last_name='%s', emails='%s' insert_date='%s', valid_till_date='%s')>" % (
                                self.username, self.first_name.value, self.last_name.value, [x.value for x in self.emails], self.insert_date, self.valid_till_date)

class ContactFirstName(Base):
    __tablename__ = 'contact_first_name'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    value = Column(String, nullable=False)
    insert_date = Column(DateTime(), server_default=func.now())
    valid_till_date = Column(DateTime(), nullable=True)
    
    def __repr__(self):
        return "<ContactFirstName(value='%s')>" % self.value
    
class ContactLastName(Base):
    __tablename__ = 'contact_last_name'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    value = Column(String, nullable=False)
    insert_date = Column(DateTime(), server_default=func.now())
    valid_till_date = Column(DateTime(), nullable=True)
    
    def __repr__(self):
        return "<ContactLastName(value='%s')>" % self.value
    
class ContactEmail(Base):
    __tablename__ = 'contact_emails'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    value = Column(String, nullable=False)
    insert_date = Column(DateTime(), server_default=func.now())
    valid_till_date = Column(DateTime(), nullable=True)
    
    contact = relationship("Contact", back_populates="emails")
    
    def __repr__(self):
        return "<ContactEmail(value='%s')>" % self.value

Base.metadata.create_all(engine)

#Celery Task
@celery.task(name='celery_worker.create')
def create_random_contact():
		username = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
		first_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
		last_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
		email = ''.join(choice(ascii_uppercase) for i in range(23)) + "@gmail.com"
		
		new_contact = Contact(
        username=username,
        first_name=ContactFirstName(value=first_name),
        last_name=ContactLastName(value=last_name),
        emails=[ContactEmail(value=email)]
    )
    
		session.add(new_contact)
		session.commit()
		return f'{username} created'
    
#Celery Task
@celery.task(name='celery_worker.delete')
def delete_old_contact():
    server_current_time = session.execute(select([func.now()])).fetchone()[0]
    one_minute_ago = server_current_time - timedelta(seconds=60)
    old_contacts = session.query(Contact).filter(Contact.insert_date <= one_minute_ago).filter_by(valid_till_date = None)
    updated_count = old_contacts.count()
    old_contacts.update({Contact.valid_till_date:func.now()}, synchronize_session=False)
    
    session.commit()
    return f'{updated_count} deleted'
    
#Create random contact every 15 seconds
@periodic_task(run_every=timedelta(seconds=15))
def periodic_create_random_contact():
    return create_random_contact()
    
#Delete contacts older than 60 seconds
@periodic_task(run_every=timedelta(seconds=60))
def periodic_delete_old_contact():
    return delete_old_contact()
