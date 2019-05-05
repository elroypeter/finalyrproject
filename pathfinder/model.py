from datetime import datetime
from pathfinder import db, login_manager
from flask_login import UserMixin

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(60), index=True, unique=True)
    telephone = db.Column(db.String(60), index=True, unique=True)
    full_names= db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    police_id = db.Column(db.Integer, db.ForeignKey('police.id'))
    is_admin = db.Column(db.Boolean, default=False)
    crimescene    = db.relationship('CrimeScene', backref='casefiler', lazy=True)

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable format.')
    @password.setter
    def password(self, password):
        """
        set password to a hashed password
        """
        self.password_hash=generate_password_hash(password)

    def verify_password(self, password):
        """
        check if hashed password matches the actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Role(db.Model):
    """
    create a Role table
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class CrimeScene(db.Model):

    __tablename__ = "crimescenes"

    id          = db.Column(db.Integer, primary_key=True)
    longitude   = db.Column(db.Float, nullable=False)
    latitude    = db.Column(db.Float, nullable=False)
    decription  = db.Column(db.Text, nullable=False)
    image_file  = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id    = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    crime    = db.relationship('Crime', backref='crimescene', lazy=True)

    def serialize_to_json(self):
        return {
            'longitude'  : self.longitude,
            'latitude'   : self.latitude,
            'description': self.decription,
            'image'      : self.image_file,
            'category'   : self.category,
            'date'       : self.date_posted
        }

    def __repr__(self):
        return f"CaseFile('{self.category}', '{self.date_posted}'"

class Category(db.Model):

    __tablename__ ="categories"

    id = db.Column(db.Integer, primary_key = True)
    violet_type = db.Column(db.String, nullable=False)
    crimescene    = db.relationship('CrimeScene', backref='scene', lazy=True)
    crime    = db.relationship('Crime', backref='category', lazy=True)

class Crime(db.Model):

    __tablename__="crimes"

    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(60), nullable=False)
    category_id    = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    scene_id    = db.Column(db.Integer, db.ForeignKey('crimescenes.id'), nullable=False)

class Police(db.Model):

    __tablename__ = "police"

    id = db.Column(db.Integer, primary_key = True)
    StationName = db.Column(db.String(100), nullable=False)
    division = db.Column(db.String(60), nullable=False)
    crimescene    = db.relationship('CrimeScene', backref='policeonscene', lazy=True)
