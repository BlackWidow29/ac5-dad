from app import db


class Endereco(db.Model):
    __tablename__ = "tbEndereco"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cep = db.Column(db.String, nullable=False, unique=True)
    logradouro = db.Column(db.String, nullable=False)
    bairro = db.Column(db.String, nullable=False)
    cidade = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
    complemento = db.Column(db.String, nullable=False)

    def __init__(self, cep, logradouro, bairro, cidade, estado, complemento):
        self.cep = cep
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.complemento = complemento