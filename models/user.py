import sqlite3

from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    # save the user to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # delete the user from the database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # get a user from the database by its name
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # get a user from the database by its id
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()