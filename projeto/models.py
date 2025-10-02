from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

# Inicialização das Extensões (sem associar ao app ainda)
db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, UserMixin):
    """Modelo para usuários, implementa A02 com hash de senha."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    # A02: Coluna para armazenar o HASH seguro da senha (60 caracteres para Bcrypt)
    password = db.Column(db.String(60), nullable=False) 
    
    # Relação com os itens que o usuário criou
    items = db.relationship('Item', backref='owner', lazy=True)

    def set_password(self, password):
        """A02: Cria o hash seguro da senha usando Bcrypt."""
        # decode('utf-8') é necessário para armazenar o hash como string
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """A02: Verifica a senha comparando o texto simples com o hash armazenado."""
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}')"

class Item(db.Model):
    """Modelo para os itens que serão criados via CRUD."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    
    # A01: Chave estrangeira que vincula o Item ao seu User. Necessário para controle de acesso.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Item('{self.name}', 'Owner ID: {self.user_id}')"