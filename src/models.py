from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  
    email = db.Column(db.String(120), nullable=False, unique=True)  
    password = db.Column(db.String(80), nullable=False) 
    is_active = db.Column(db.Boolean(), nullable=False)
    
    favorites = db.relationship('UserFavorite', back_populates='user')

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
        }

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
        }

class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    favorites = db.relationship('UserFavorite', back_populates='character')
    
    def __repr__(self):
        return f'<Character {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Planet(db.Model):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    favorites = db.relationship('UserFavorite', back_populates='planet')
    
    def __repr__(self):
        return f'<Planet {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class UserFavorite(db.Model):
    __tablename__ = 'user_favorites'

    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='favorites')

    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    character = db.relationship('Character', back_populates='favorites')
    
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    planet = db.relationship('Planet', back_populates='favorites')

    def __repr__(self):
        return f'<UserFavorite User {self.user_id}, Character {self.character_id}, Planet {self.planet_id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        }

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        }
