"""
Routes modul definierar API-rutterna för användarhantering med CRUD-operationer.
Den visar endpoints för att skapa, läsa, uppdatera och ta bort användare.
"""


from flask import Blueprint, request, jsonify, current_app  
from user_controller import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)  # Importerar funktioner från user_controller
from auth_routes import token_required  # Importerar autentiseringskrav från auth_routes

# Skapa en Blueprint för användarrutter (grupperar relaterade rutter)
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/', methods=['GET'])
@token_required  # Kräver giltig autentiseringstoken
def get_users():
    """
    Slutpunkt för att hämta alla användare.
    
    Kräver: Autentiseringstoken
    
    Returnerar:
        JSON-svar med lista över användare
    """
    # Hämta databasanslutning från app-kontext
    db_connection = current_app.config['DB_CONNECTION']
    
    # Hämta alla användare från databasen
    users = get_all_users(db_connection)
    
    # Kontrollera om hämtningen lyckades
    if users is not None:
        return jsonify({
            'status': 'success',
            'data': users
        }), 200  # OK statuskod
    else:
        return jsonify({
            'status': 'error',
            'message': 'Kunde inte hämta användare'
        }), 500  # Internal Server Error statuskod

@users_bp.route('/<int:user_id>', methods=['GET'])
@token_required  # Kräver giltig autentiseringstoken
def get_user(user_id):
    """
    Slutpunkt för att hämta en specifik användare via ID.
    
    Kräver: Autentiseringstoken
    
    Argument:
        user_id (int): ID för användaren som ska hämtas
    
    Returnerar:
        JSON-svar med användardata om den hittas
    """
    # Hämta databasanslutning från app-kontext
    db_connection = current_app.config['DB_CONNECTION']
    
    # Hämta specifik användare från databasen
    user = get_user_by_id(user_id, db_connection)
    
    # Kontrollera om användaren hittades
    if user:
        return jsonify({
            'status': 'success',
            'data': user
        }), 200  # OK statuskod
    else:
        return jsonify({
            'status': 'error',
            'message': 'Användaren hittades inte'
        }), 404  # Not Found statuskod

@users_bp.route('/', methods=['POST'])
@token_required  # Kräver giltig autentiseringstoken
def add_user():
    """
    Endpoint för att skapa en ny användare.
    
    Kräver: Autentiseringstoken och administratörsbehörighet
    
    Förväntar sig JSON med:
        - username: Önskat användarnamn
        - password: Önskat lösenord
        - email: Användarens e-post
        - name (valfritt): Användarens fullständiga namn
    
    Returnerar:
        JSON-svar med status för användarens skapande
    """
    # Kontrollera om den begärande användaren är en administratör
    # Detta är ett enkelt exempel - i verkligheten skulle du kontrollera användarroller
    if 'user_id' in request.user and request.user['user_id'] != 1:  # Antar att user_id 1 är admin
        return jsonify({
            'status': 'error',
            'message': 'Administratörsbehörighet krävs'
        }), 403  # Forbidden statuskod
    
    # Hämta JSON-data från förfrågan
    data = request.get_json()
    
    # Validera förfrågningsdata
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Ingen data tillhandahållen'
        }), 400  # Bad Request statuskod
    
    # Hämta databasanslutning från app-kontext
    db_connection = current_app.config['DB_CONNECTION']
    
    # Skapa användare
    result = create_user(data, db_connection)
    
    # Returnera resultatet baserat på om skapandet lyckades eller inte
    if result['status'] == 'success':
        return jsonify(result), 201  # Created statuskod
    else:
        if 'finns redan' in result.get('message', ''):
            return jsonify(result), 409  # Conflict statuskod
        else:
            return jsonify(result), 400  # Bad Request statuskod

@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_required  # Kräver giltig autentiseringstoken
def update_user_route(user_id):
    """
    Slutpunkt för att uppdatera en användare.
    
    Kräver: Autentiseringstoken
    
    Argument:
        user_id (int): ID för användaren som ska uppdateras
    
    Förväntar sig JSON med någon av:
        - email: Ny e-post
        - name: Nytt namn
        - password: Nytt lösenord
    
    Returnerar:
        JSON-svar med status för användaruppdateringen
    """
    # Kontrollera om den begärande användaren uppdaterar sin egen profil eller är en administratör
    if 'user_id' in request.user and request.user['user_id'] != user_id and request.user['user_id'] != 1:
        return jsonify({
            'status': 'error',
            'message': 'Du kan bara uppdatera din egen profil om du inte är administratör'
        }), 403  # Forbidden statuskod
    
    # Hämta JSON-data från förfrågan
    data = request.get_json()
    
    # Validera förfrågningsdata
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Ingen data tillhandahållen'
        }), 400  # Bad Request statuskod
    
    # Hämta databasanslutning från app-kontext
    db_connection = current_app.config['DB_CONNECTION']
    
    # Uppdatera användare
    result = update_user(user_id, data, db_connection)
    
    # Returnera resultatet baserat på om uppdateringen lyckades eller inte
    if result['status'] == 'success':
        return jsonify(result), 200  # OK statuskod
    else:
        if 'hittades inte' in result.get('message', ''):
            return jsonify(result), 404  # Not Found statuskod
        else:
            return jsonify(result), 400  # Bad Request statuskod

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required  # Kräver giltig autentiseringstoken
def delete_user_route(user_id):
    """
    Endpoint för att ta bort en användare.
    
    Kräver: Autentiseringstoken och administratörsbehörighet
    
    Argument:
        user_id (int): ID för användaren som ska tas bort
    
    Returnerar:
        JSON-svar med status för användarborttagningen
    """
    # Kontrollera om den begärande användaren är en administratör
    if 'user_id' in request.user and request.user['user_id'] != 1:
        return jsonify({
            'status': 'error',
            'message': 'Administratörsbehörighet krävs'
        }), 403  # Forbidden statuskod
    
    # Hämta databasanslutning från app-kontext
    db_connection = current_app.config['DB_CONNECTION']
    
    # Ta bort användare
    result = delete_user(user_id, db_connection)
    
    # Returnera resultatet baserat på om borttagningen lyckades eller inte
    if result['status'] == 'success':
        return jsonify(result), 200  # OK statuskod
    else:
        if 'hittades inte' in result.get('message', ''):
            return jsonify(result), 404  # Not Found statuskod
        else:
            return jsonify(result), 500  # Internal Server Error statuskod

@users_bp.route('/profile', methods=['GET'])
@token_required  # Kräver giltig autentiseringstoken
def get_own_profile():
    """
    Endpoint för en användare att hämta sin egen profil.
    
    Kräver: Autentiseringstoken
    
    Returnerar:
        JSON-svar med den autentiserade användarens profildata
    """
    # Hämta användar-ID från token
    user_id = request.user['user_id']
    
    # Hämta databasanslutning från app-kontext
    db_connection = current_app.config['DB_CONNECTION']
    
    # Hämta användardata
    user = get_user_by_id(user_id, db_connection)
    
    # Kontrollera om användaren hittades
    if user:
        return jsonify({
            'status': 'success',
            'data': user
        }), 200  # OK statuskod
    else:
        return jsonify({
            'status': 'error',
            'message': 'Användaren hittades inte'
        }), 404  # Not Found statuskod