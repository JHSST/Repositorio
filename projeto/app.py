from flask import Flask, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, bcrypt, User, Item # Importamos as classes do models.py

# --- Configuração da Aplicação ---
app = Flask(__name__)
# Chave secreta CRUCIAL para segurança de sessão e proteção CSRF
app.config['SECRET_KEY'] = 'chave_de_producao_forte_mude_isto_agora' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa as extensões com a instância do app
db.init_app(app)
bcrypt.init_app(app) # Inicializa o Bcrypt para A02
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Rota para onde redirecionar se precisar de login

# --- Configuração do Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    """Carrega o usuário para o Flask-Login"""
    return User.query.get(int(user_id))

# --- Criação do Banco de Dados ---
# Cria as tabelas User e Item se não existirem
with app.app_context():
    db.create_all()


# ======================================================================
# ROTAS DE AUTENTICAÇÃO (LOGIN/REGISTRO) - Necessário para A01 e A02
# ======================================================================

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Usuário já existe"}), 409
    
    # A02: O método set_password garante o hash seguro
    new_user = User(username=username)
    new_user.set_password(password) 

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuário registrado com sucesso! (A02 mitigado)"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    # A02: O método check_password verifica a senha de forma segura
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": f"Login bem-sucedido. Bem-vindo, {user.username}"})
    
    return jsonify({"message": "Credenciais inválidas"}), 401

@app.route('/logout')
@login_required # Garante que a sessão exista para fazer logout
def logout():
    logout_user()
    return jsonify({"message": "Logout bem-sucedido"})


# ======================================================================
# ROTAS CRUD DOS ITENS (Create, Read, Update, Delete) - Foco em A01
# ======================================================================

# --- CREATE (C) ---
@app.route('/items', methods=['POST'])
@login_required # A01: Apenas autenticados podem criar
def create_item():
    data = request.json
    
    new_item = Item(
        name=data.get('name'), 
        description=data.get('description'),
        # A01: Associa o item ao ID do usuário logado
        user_id=current_user.id 
    )
    
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item criado", "id": new_item.id}), 201

# --- READ ALL (R) ---
@app.route('/items', methods=['GET'])
@login_required
def get_all_items():
    # A01: Mitigação ao mostrar APENAS os itens pertencentes ao usuário logado
    items = Item.query.filter_by(user_id=current_user.id).all()
    
    output = []
    for item in items:
        output.append({
            'id': item.id, 
            'name': item.name, 
            'description': item.description,
            'owner_id': item.user_id
        })

    return jsonify(output)

# --- READ ONE (R) ---
@app.route('/items/<int:item_id>', methods=['GET'])
@login_required
def get_one_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    # A01: Broken Access Control Check: verifica se o item pertence ao usuário logado
    if item.user_id != current_user.id:
        return jsonify({"message": "Acesso negado. Você não é o dono deste item. (A01 mitigado)"}), 403 

    return jsonify({
        'id': item.id, 
        'name': item.name, 
        'description': item.description,
        'owner_id': item.user_id
    })

# --- UPDATE (U) ---
@app.route('/items/<int:item_id>', methods=['PUT'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.json
    
    # A01: Broken Access Control Check: Apenas o dono pode atualizar
    if item.user_id != current_user.id:
        return jsonify({"message": "Acesso negado. Você não é o dono deste item. (A01 mitigado)"}), 403 

    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    
    db.session.commit()
    return jsonify({"message": "Item atualizado com sucesso!"})

# --- DELETE (D) ---
@app.route('/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    # A01: Broken Access Control Check: Apenas o dono pode deletar
    if item.user_id != current_user.id:
        return jsonify({"message": "Acesso negado. Você não é o dono deste item. (A01 mitigado)"}), 403 

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deletado com sucesso!"})


# --- EXECUÇÃO: A solução para evitar erros de shell no Windows ---
# Ao executar o arquivo diretamente com 'python app.py', este bloco é chamado.
if __name__ == '__main__':
    print("--- Servidor Iniciado ---")
    print("Para Testes, use: http://127.0.0.1:5000/")
    app.run(debug=True)