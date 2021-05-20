from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    # nome da tabela
    __tablename__ = "user"

    # campos da tabela
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


# class Orcamento(db.Model):
#     __tablename__ = "tbOrcamento"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     nome_cliente = db.Column(db.String(100))
#     taxa_auxiliar = db.Column(db.Integer)
#     observacoes = db.Column(db.String(255))
#     valor_total = db.Column(db.Float)
#
#     def __init__(self, nome_cliente, taxa_auxiliar, observacoes, valor_total):
#         self.nome_cliente = nome_cliente
#         self.taxa_auxiliar = taxa_auxiliar
#         self.observacoes = observacoes
#         self.valor_total = valor_total


class Material(db.Model):
    __tablename__ = "tbMaterial"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preco = db.Column(db.Float)
    descricao = db.Column(db.String(255))
    tipo = db.Column(db.String(50))

    def __init__(self, preco, descricao, tipo):
        self.preco = preco
        self.descricao = descricao
        self.tipo = tipo


class Servico(db.Model):
    __tablename__ = "tbServico"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255))
    valor_mao_de_obra = db.Column(db.Float)
    valor_total = db.Column(db.Float)

    def __init__(self, descricao, valor_mao_de_obra, valor_total):
        self.descricao = descricao
        self.valor_mao_de_obra = valor_mao_de_obra
        self.valor_total = valor_total


class MaterialServico(db.Model):
    __tablename__ = "tbMaterialServico"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_material = db.Column(db.Integer, db.ForeignKey('tbMaterial.id'))
    id_servico = db.Column(db.Integer, db.ForeignKey('tbServico.id'))

    def __init__(self, id_material, id_servico):
        self.id_material = id_material
        self.id_servico = id_servico

db.create_all()
