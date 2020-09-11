from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    # table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # the items in the store
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    # JSON-representation of the class object
    def json(self):
        return {
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }

    # get a store from the database by its name
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # save the store to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # remove the store from the database
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()