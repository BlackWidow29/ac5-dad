from app import app, db

class Orcamento(db.model):
    __tablename__ = "tbOrcamento"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cliente = db.Column(db.String(100))
    taxa_auxiliar = db.Column(db.Integer)
    observacoes = db.Column(db.String(255))
    valor_total = db.Column(db.Float)

    def __init__(self, nome_cliente, taxa_auxiliar, observacoes,valor_total):
        self.nome_cliente = nome_cliente
        self.taxa_auxiliar = taxa_auxiliar
        self.observacoes = observacoes
        self.valor_total = valor_total
