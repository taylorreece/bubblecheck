from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__  = True
    id       = db.Column(db.Integer, primary_key=True)
    created  = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        db.session.add(self)
        db.session.commit()

# Define a User model
class User(Base):
    __tablename__ = 'users'
    name     = db.Column(db.Text(), nullable=False)
    email    = db.Column(db.Text(), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password):
        self.name     = name
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)
