from app import db

class Orcamento(db.Model):
    __tablename__ = "tbOrcamento"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column(db.String(100))
    observacoes = db.Column(db.String(255))
    valor_total = db.Column(db.Float)
    numero_endereco = db.Column(db.Integer)
    id_endereco = db.Column(db.Integer, db.ForeignKey('tbEndereco.id'))

    def __init__(self, nome_cliente, observacoes, valor_total, numero_endereco, id_endereco):
        self.nome_cliente = nome_cliente
        self.observacoes = observacoes
        self.valor_total = valor_total
        self.numero_endereco = numero_endereco
        self.id_endereco = id_endereco