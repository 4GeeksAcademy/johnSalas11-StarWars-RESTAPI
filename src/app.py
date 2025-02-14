"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, UserFavorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def handle_get_characters():
    all_characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), all_characters))
    return jsonify(all_characters), 200

@app.route('/characters/<int:id>', methods=['GET'])
def handle_get_character(id):
    character = Character.query.get(id)
    if character is None:
        return jsonify({'msg': 'Character not found'}), 404
    return jsonify(character.serialize()), 200

@app.route('/planets', methods=['GET'])
def handle_get_planets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    return jsonify(all_planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def handle_get_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({'msg': 'Planet not found'}), 404
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def handle_get_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
    return jsonify(all_users), 200

@app.route('/users/<int:id>', methods=['GET'])
def handle_get_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify(user.serialize()), 200

@app.route('/favorites', methods=['GET'])
def handle_get_favorites():
    all_characters = UserFavorite.query.all()
    all_characters = list(map(lambda x: x.serialize(), all_characters))
    return jsonify(all_characters), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.first()  
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'msg': 'Planet not found'}), 404
    
    new_favorite = UserFavorite(user_id=user.id, planet_id=planet.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Planet added to favorites"}), 201

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user = User.query.first()  
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({'msg': 'Character not found'}), 404
    
    new_favorite = UserFavorite(user_id=user.id, character_id=character.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg": "Character added to favorites"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user = User.query.first()  
    favorite = UserFavorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({'msg': 'Favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Planet removed from favorites"}), 200

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(character_id):
    user = User.query.first()  
    favorite = UserFavorite.query.filter_by(user_id=user.id, character_id=character_id).first()
    if favorite is None:
        return jsonify({'msg': 'Favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Character removed from favorites"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
