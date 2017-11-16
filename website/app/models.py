from app import db

if db.engine.name == 'postgresql':
    from app.sqlalchemy_extensions.uuid_column import UUID
    id_column_type = UUID
    id_column_server_default = db.text("uuid_in(md5(random()::text || now()::text)::cstring)")
else:
    id_column_type = db.Integer
    id_column_server_default = None
# Define a base model for other database tables to inherit
# We'll use UUIDs in postgresql, but just ids for testing
class Base(db.Model):
    __abstract__  = True
    id = db.Column(id_column_type, primary_key=True, server_default=id_column_server_default)
    created  = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp())
    modified = db.Column(db.DateTime(timezone=True), nullable=False, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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
