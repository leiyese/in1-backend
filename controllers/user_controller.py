from flask import session
from models import User


def user_auth():
    if "user_id" in session:
        user_id = session["user_id"]
        user = User.query.filter_by(id=user_id).first()
        return user
    else:
        return False
    
    
def login_check(username, password):
    if not username or not password:
        flash("Please fill in both fields!")
        return redirect(url_for("login"))
    user = User.query.filter_by(username=username.lower()).first()
    if user:
        if check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect(url_for("index"))
        else:
            flash("Incorrect password!")
            return redirect(url_for("login"))
    else:
        flash("Incorrect username!")
        return redirect(url_for("login"))
    
    
def register_user(username, password):
    if not username or not password:
        flash("Username and Password are required for registration!")
        return redirect(url_for("register"))
    existing_user = User.query.filter_by(username=username.lower()).first()
    if existing_user:
        flash("Username is already in use! Please choose another.")
        return redirect(url_for("register"))
    if len(password)<=7:
        flash("Password must be atleast 8 characters!")
        return redirect(url_for("register"))
    password_hash= generate_password_hash(password)
    user = User(username=username.lower(), password_hash=password_hash, admin=False)
    db.session.add(user)
    db.session.commit()
    flash("Registration is successful! Please login.", "success")
    return redirect(url_for("login"))
