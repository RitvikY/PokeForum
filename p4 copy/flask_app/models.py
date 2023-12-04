from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from mongoengine import Document, StringField, ReferenceField, DateTimeField, ListField


@login_manager.user_loader
def load_user(username):
    return User.objects(username=username).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField(default='default.jpg')  # Assuming there is a default image

    # Returns unique string identifying our object
    def get_id(self):
        return str(self.username)  


from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime
from .extensions import db  # Make sure this import points to wherever you initialize MongoEngine






class Reply(Document):
    content = StringField(required=True)
    author = ReferenceField('User')  # Use string reference
    posted_at = DateTimeField(default=datetime.utcnow)
    review = ReferenceField('Review')  # Use string reference instead of direct class reference

class Review(Document):
    content = StringField(required=True)
    author = ReferenceField('User')  # Use string reference
    pokemon_name = StringField(required=True)
    posted_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'replies'}
    replies = ListField(ReferenceField('Reply'))

