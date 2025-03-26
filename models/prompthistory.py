from config.db import db

#initial structure of the Prompthistory model

class Prompthistory(db.Model):
    __tablename__ = 'prompthistories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ai_id = db.Column(db.Integer, db.ForeignKey('ai_models.id'), nullable=False)
    prompt = db.Column(db.String(255), nullable=False)
    prompt_response = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f"<Prompthistory {self.prompt}>"
