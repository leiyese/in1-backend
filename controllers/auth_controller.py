"""
Auth modul lägger till funktioner för att autentisera user och hantera user sessiones
Den hanterar inloggningsvalidering, token-generering och autentiseringsrelaterade operationer.
"""

import bcrypt  # För att hasha lösenord på ett säkert sätt vet ej om vi ska ha bcrypt men jag la till den kan ta bort detta om vi inte vill ha bcrypt
import jwt  # För att skapa och verifiera Tokens
from datetime import datetime, timedelta  # För att hantera datum och tid för token-giltighet
import os  # För att interagera med operativsystemet, som att hämta miljövariabler
from flask import jsonify  

# I en produktionsmiljö bör detta komma från miljövariabler för säkerhet det verkar vara standard prectis men kanske är overkill för vårat projekt
SECRET_KEY = "your_secret_key_here"  # Hemlig nyckel för att signera tokens
TOKEN_EXPIRY = 24  # Token-giltighetstid i timmar

def authenticate_user(username, password, db_connection):
    """
    Autentisera en user genom att verifiera deras inloggningsuppgifter.
    
    Argument:
        username (str): Användarnamnet som användaren anger
        password (str): Lösenordet som användaren anger
        db_connection: Databasanslutningsobjekt
    
    Returnerar:
        dict: Användardata och token om autentiseringen lyckas, eller felmeddelande
    """
    # Hämta användardata från databasen
    cursor = db_connection.cursor(dictionary=True)  # Skapar en cursor för att utföra databasfrågor
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))  # SQL-fråga för att hitta användaren
    user = cursor.fetchone()  # Hämtar användarens datarad
    cursor.close()  # Stänger databasanslutningen
    
    # Kontrollera om användaren finns och lösenordet är korrekt
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        # Om autentiseringen lyckas, generera en token
        token = generate_token(user['id'])
        return {
            'status': 'success',
            'token': token,
            'user_id': user['id'],
            'username': user['username']
        }
    else:
        # Om autentiseringen misslyckas, returnera ett felmeddelande
        return {
            'status': 'error',
            'message': 'Ogiltigt användarnamn eller lösenord'
        }

def generate_token(user_id):
    """
    Generera en JWT-token för en autentiserad användare.
    
    Argument:
        user_id (int): Den unika identifieraren för den autentiserade användaren
    
    Returnerar:
        str: JWT-token
    """
    # Skapa payload för token med användar-ID och utgångstid
    payload = {
        'user_id': user_id,  # Användarens ID lagras i token
        'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY),  # Tidpunkt då token upphör att gälla jag vet inte varför utcnow blir överstruket men fick fram att ddet kan bero på att vissa linters markerar datetime.utcnow() som deprecated och föreslår datetime.now(timezone.utc)
        'iat': datetime.utcnow()  # Tidpunkt då token genererades
    }
    # Skapa och returnera den signerade token
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """
    Verifiera giltigheten för en JWT-token.
    
    Argument:
        token (str): JWT-token att verifiera
    
    Returnerar:
        dict: Den avkodade payload om giltig, eller felmeddelande
    """
    try:
        # Försök avkoda token för att verifiera den
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return {'status': 'success', 'payload': payload}
    except jwt.ExpiredSignatureError:
        # Om token har gått ut
        return {'status': 'error', 'message': 'Token har gått ut'}
    except jwt.InvalidTokenError:
        # Om token är ogiltig av någon annan anledning
        return {'status': 'error', 'message': 'Ogiltig token'}

def hash_password(password):
    """
    Hasha ett lösenord för säker lagring.
    
    Argument:
        password (str): Lösenordet i klartext som ska hashas
    
    Returnerar:
        str: Det hashade lösenordet
    """
    # Skapa en slumpmässig salt för extra säkerhet
    salt = bcrypt.gensalt()
    # Hasha lösenordet med salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    # Returnera det hashade lösenordet som en sträng
    return hashed.decode('utf-8')