"""
controller modul för att hantera användardata med CRUD-operationer.

"""

# Importerar nödvändiga bibliotek
from flask import jsonify  
import bcrypt  # För att hantera lösenordshashning som jag skrev i auth tog med detta vet inte om vi ska ha bcrypt
from auth_controller import hash_password  # Importerar hashningsfunktion från auth_controller

def get_all_users(db_connection):
    """
    Hämta alla användare från databasen.
    
    Argument:
        db_connection: Databasanslutningsobjekt
    
    Returnerar:
        list: Lista med users  (exklusive lösenordshash)
    """
    # Skapar en databasmarkör för att köra SQL-frågor
    cursor = db_connection.cursor(dictionary=True)  # Returnerar resultat som dictionaries
    try:
        # Utför SQL-fråga för att hämta alla användare (utan lösenordshash för säkerhet)
        cursor.execute("SELECT id, username, email, name, created_at, updated_at FROM users")
        users = cursor.fetchall()  # Hämtar alla rader med resultat
        return users
    except Exception as e:
        # Om något fel uppstår under frågan
        return None
    finally:
        # Stänger alltid databasmarkören för att förhindra minnesläckor
        cursor.close()

def get_user_by_id(user_id, db_connection):
    """
    Hämta en specifik användare via ID.
    
    Argument:
        user_id (int): Den unika identifieraren för användaren
        db_connection: Databasanslutningsobjekt
    
    Returnerar:
        dict: Userdata om den hittas (exklusive lösenordshash), annars None
    """
    # Skapar en databasmarkör för att köra SQL-frågor
    cursor = db_connection.cursor(dictionary=True)
    try:
        # Utför SQL-fråga för att hämta en specifik användare med ID
        cursor.execute(
            "SELECT id, username, email, name, created_at, updated_at FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()  # Hämtar en rad med resultat
        return user
    except Exception as e:
        # Om något fel uppstår under frågan
        return None
    finally:
        # Stänger alltid databasmarkören
        cursor.close()

def create_user(user_data, db_connection):
    """
    Skapa en ny user i databasen.
    
    Argument:
        user_data (dict): Ordbok med user information
        db_connection: Databasanslutningsobjekt
    
    Returnerar:
        dict: Statusmeddelande och nytt användar-ID om det lyckas
    """
    # Kontrollera att all nödvändig data finns
    if not all(key in user_data for key in ['username', 'password', 'email']):
        return {
            'status': 'error',
            'message': 'Användarnamn, lösenord och e-post krävs'
        }
    
    # Skapar en databasmarkör
    cursor = db_connection.cursor()
    try:
        # Kontrollera om användarnamnet redan finns
        cursor.execute("SELECT id FROM users WHERE username = %s", (user_data['username'],))
        if cursor.fetchone():
            return {
                'status': 'error',
                'message': 'Användarnamnet finns redan'
            }
        
        # Kontrollera om e-postadressen redan finns
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_data['email'],))
        if cursor.fetchone():
            return {
                'status': 'error',
                'message': 'E-postadressen finns redan'
            }
        
        # Hasha lösenordet för säker lagring
        hashed_password = hash_password(user_data['password'])
        
        # Infoga ny användare i databasen
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, email, name, created_at)
            VALUES (%s, %s, %s, %s, NOW())
            """,
            (
                user_data['username'],
                hashed_password,
                user_data['email'],
                user_data.get('name', '')  # Använder tomt värde om namn inte anges
            )
        )
        db_connection.commit()  # Spara ändringar i databasen
        
        # Hämta ID för den nyligen skapade användaren
        user_id = cursor.lastrowid
        
        return {
            'status': 'success',
            'message': 'Användare skapad framgångsrikt',
            'user_id': user_id
        }
    except Exception as e:
        # Ångra ändringar om ett fel uppstår
        db_connection.rollback()
        return {
            'status': 'error',
            'message': f'Ett fel uppstod när användaren skulle skapas: {str(e)}'
        }
    finally:
        # Stänger alltid databasmarkören
        cursor.close()

def update_user(user_id, update_data, db_connection):
    """
    Uppdatera en befintlig användares information.
    
    Argument:
        user_id (int): Den unika identifieraren för användaren som ska uppdateras
        update_data (dict): fält som ska uppdateras
        db_connection: Databasanslutningsobjekt
    
    Returnerar:
        dict: Statusmeddelande som indikerar hur det gick
    """
    # Kontrollera om användaren finns
    cursor = db_connection.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return {
                'status': 'error',
                'message': 'Användaren hittades inte'
            }
        
        # Förbered uppdateringsfrågan
        update_fields = []  # Lista med fält som ska uppdateras
        values = []  # Lista med värden för uppdatering
        
        # Bearbeta uppdaterbara fält
        if 'email' in update_data:
            update_fields.append("email = %s")
            values.append(update_data['email'])
            
        if 'name' in update_data:
            update_fields.append("name = %s")
            values.append(update_data['name'])
            
        if 'password' in update_data:
            update_fields.append("password_hash = %s")
            hashed_password = hash_password(update_data['password'])
            values.append(hashed_password)
        
        # Lägg till uppdateringstidsstämpel
        update_fields.append("updated_at = NOW()")
        
        # Om inga fält ska uppdateras, avsluta tidigt
        if not update_fields:
            return {
                'status': 'error',
                'message': 'Inga fält att uppdatera'
            }
        
        # Bygg och kör SQL-frågan
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
        values.append(user_id)
        
        cursor.execute(query, tuple(values))
        db_connection.commit()  # Spara ändringar i databasen
        
        return {
            'status': 'success',
            'message': 'Användare uppdaterad framgångsrikt'
        }
    except Exception as e:
        # Ångra ändringar om ett fel uppstår
        db_connection.rollback()
        return {
            'status': 'error',
            'message': f'Ett fel uppstod när användaren skulle uppdateras: {str(e)}'
        }
    finally:
        # Stänger alltid databasmarkören
        cursor.close()

def delete_user(user_id, db_connection):
    """
    Ta bort en användare från databasen.
    
    Argument:
        user_id (int): Den unika identifieraren för användaren som ska tas bort
        db_connection: Databasanslutningsobjekt
    
    Returnerar:
        dict: Statusmeddelande som indikerar framgång eller misslyckande
    """
    cursor = db_connection.cursor()
    try:
        # Kontrollera om användaren finns
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return {
                'status': 'error',
                'message': 'Användaren hittades inte'
            }
        
        # Ta bort användaren
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db_connection.commit()  # Spara ändringar i databasen
        
        return {
            'status': 'success',
            'message': 'Användare raderad framgångsrikt'
        }
    except Exception as e:
        # Ångra ändringar om ett fel uppstår
        db_connection.rollback()
        return {
            'status': 'error',
            'message': f'Ett fel uppstod när användaren skulle raderas: {str(e)}'
        }
    finally:
        # Stänger alltid databasmarkören
        cursor.close()