from app import db


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
