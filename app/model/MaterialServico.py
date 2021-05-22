from app import db

class MaterialServico(db.Model):
    __tablename__ = "tbMaterialServico"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_material = db.Column(db.Integer, db.ForeignKey('tbMaterial.id'))
    id_servico = db.Column(db.Integer, db.ForeignKey('tbServico.id'))

    def __init__(self, id_material, id_servico):
        self.id_material = id_material
        self.id_servico = id_servico
