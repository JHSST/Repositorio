from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    # A02: A coluna 'password' armazenará o HASH seguro (String longa)
    password = db.Column(db.String(60), nullable=False) 
    
    # Relação com os itens que o usuário criou
    items = db.relationship('Item', backref='owner', lazy=True)

    def set_password(self, password):
        """A02: Cria o hash seguro da senha antes de salvar."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """A02: Verifica a senha comparando com o hash."""
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}')"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    
    # A01: Chave estrangeira que liga o Item ao seu dono (User)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Item('{self.name}', 'Owner ID: {self.user_id}')"