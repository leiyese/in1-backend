"""
Auth routes modul definierar API-rutterna för autentiseringsrelaterade operationer.
Den inkluderar endpoints för inloggning, registrering och token-validering.
"""

# Importerar nödvändiga bibliotek och moduler
from flask import Blueprint, request, jsonify, current_app  # Flask-komponenter för att bygga API:er
from auth_controller import authenticate_user, hash_password, verify_token  # Importerar funktioner från auth_controller

# Skapa en Blueprint för autentiseringsrutter (grupperar relaterade rutter)
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint för användarinloggning.
    
    Förväntar sig JSON med:
        - username: Användarens användarnamn
        - password: Användarens lösenord
    
    Returnerar:
        JSON-svar med autentiseringstoken om det lyckas
    """
    # Hämta JSON-data från förfrågan
    data = request.get_json()
    
    # Validera förfrågningsdata
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Användarnamn och lösenord krävs'
        }), 400  # Bad Req statuskod
    
    # Hämta databasanslutning från app-kontext
    db_connection = current_app.config['DB_CONNECTION']
    
    # Autentisera användaren
    result = authenticate_user(data['username'], data['password'], db_connection)
    
    # Returnera resultatet baserat på om autentiseringen lyckades eller inte
    if result['status'] == 'success':
        return jsonify(result), 200  # OK statuskod
    else:
        return jsonify(result), 401  # Unauthorized statuskod

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint för user registrering.
    
    Förväntar sig JSON med:
        - username: Önskat användarnamn
        - password: Önskat lösenord
        - email: Användarens e-post
        - name: Användarens fullständiga namn (valfritt)
    
    Returnerar:
        JSON-svar med status för registrering
    """
    # Hämta JSON-data från förfrågan
    data = request.get_json()
    
    # Validera förfrågningsdata
    if not data or 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Användarnamn, lösenord och e-post krävs'
        }), 400  # Bad Request statuskod
    
    # Hämta databasanslutning från app-kontext
    db_connection = current_app.config['DB_CONNECTION']
    cursor = db_connection.cursor()
    
    try:
        # Kontrollera om användarnamnet redan finns
        cursor.execute("SELECT id FROM users WHERE username = %s", (data['username'],))
        if cursor.fetchone():
            return jsonify({
                'status': 'error',
                'message': 'Användarnamnet finns redan'
            }), 409  # Conflict statuskod
        
        # Kontrollera om e-postadressen redan finns
        cursor.execute("SELECT id FROM users WHERE email = %s", (data['email'],))
        if cursor.fetchone():
            return jsonify({
                'status': 'error',
                'message': 'E-postadressen finns redan'
            }), 409  # Conflict statuskod
        
        # Hasha lösenordet för säker lagring
        hashed_password = hash_password(data['password'])
        
        # Skapa ny användare i databasen
        cursor.execute(
            "INSERT INTO users (username, password_hash, email, name, created_at) VALUES (%s, %s, %s, %s, NOW())",
            (data['username'], hashed_password, data['email'], data.get('name', ''))
        )
        db_connection.commit()  # Spara ändringarna i databasen
        
        return jsonify({
            'status': 'success',
            'message': 'Användare registrerad framgångsrikt'
        }), 201  # Created statuskod
        
    except Exception as e:
        # Hantera eventuella fel under registreringen
        db_connection.rollback()  # Ångra ändringar vid fel
        current_app.logger.error(f"Registreringsfel: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Ett fel uppstod under registreringen'
        }), 500  # Internal Server Error statuskod
    finally:
        cursor.close()  # Stäng cursor oavsett resultat

@auth_bp.route('/verify-token', methods=['POST'])
def validate_token():
    """
    Endpoint för att verifiera en JWT-token.
    
    Förväntar sig JSON med:
        - token: JWT-token att validera
    
    Returnerar:
        JSON-svar med token-giltighetsstatus
    """
    # Hämta JSON-data från förfrågan
    data = request.get_json()
    
    # Kontrollera att token finns i förfrågan
    if not data or 'token' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Token krävs'
        }), 400  # Bad Request statuskod
    
    # Verifiera token
    result = verify_token(data['token'])
    
    # Returnera resultatet baserat på verifieringen
    if result['status'] == 'success':
        return jsonify(result), 200  # OK statuskod
    else:
        return jsonify(result), 401  # Unauthorized statuskod

# Funktion för att skapa en middleware för routes som kräver autentisering
def token_required(f):
    """
    Funktion för att skydda rutter som kräver autentisering.
    
    Argument:
        f: Funktionen som ska dekoreras
    
    Returnerar:
        Den dekorerade funktionen som kontrollerar om en giltig token finns innan fortsättning
    """
    from functools import wraps  # Hjälpfunktion för att skapa dekoratorer
    
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Kontrollera om token finns i headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]  # Extrahera token från Authorization-header
        
        # Om ingen token hittades
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'Token saknas'
            }), 401  # Unauthorized statuskod
        
        # Verifiera token
        result = verify_token(token)
        
        # Om token inte är giltig
        if result['status'] != 'success':
            return jsonify(result), 401  # Unauthorized statuskod
        
        # Lägg till användarinformation till förfrågningskontexten för senare användning
        request.user = result['payload']
        
        # Fortsätt till den skyddade funktionen
        return f(*args, **kwargs)
    
    return decorated
