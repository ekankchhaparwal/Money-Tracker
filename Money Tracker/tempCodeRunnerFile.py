db = SQLAlchemy(app)

class Authorization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),  nullable=False)
    password = db.Column(db.String(30),  nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.id} -> {self.username} -> {self.password}"