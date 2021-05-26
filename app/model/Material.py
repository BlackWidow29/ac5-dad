from app import db


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
