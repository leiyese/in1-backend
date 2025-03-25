from config.db import db

#initial structure of the Ai_model table and ai_type table

class Ai_model(db.Model):
    __tablename__ = 'ai_models'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    ai_type_id = db.Column(db.Integer, db.ForeignKey('ai_types.id'), nullable=False)
   
    

    def __repr__(self):
        return f"<Ai_model {self.name}>"

class Ai_type(db.Model):
    __tablename__ = 'ai_types'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    type = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"<Ai_type {self.name}>"