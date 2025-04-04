from config.db import db   

#initial structure of the Corporation model

class Corporation(db.Model):
    __tablename__ = 'corporations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    subscription = db.Column(db.Boolean, default=False, nullable=False)
    business_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Corporation {self.name}>"
