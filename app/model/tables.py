from app import app, db


# class Orcamento(db.model):
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


class Material(db.model):
    __tablename__ = "tbMaterial"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    preco = db.Column(db.Float)
    cor = db.Column(db.String(100))
    descricao = db.Column(db.String(255))
    categoria = db.Column(db.String(50))
    tipo = db.Column(db.String(50))
    qtd_disponivel = db.Column(db.Integer)

    def __init__(self, preco, cor, descricao, categoria, tipo, qtd_disponivel):
        self.preco = preco
        self.cor = cor
        self.descricao = descricao
        self.categoria = categoria
        self.tipo = tipo
        self.qtd_disponivel = qtd_disponivel


class Servico(db.model):
    __tablename__ = "tbServico"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255))
    qtd_material = db.Column(db.Integer)
    valor_mao_de_obra = db.Column(db.Float)
    valor_total = db.Column(db.Float)
    qtd_metros = db.Column(db.Integer)

    def __init__(self, descricao, qtd_material, valor_mao_de_obra, valor_total, qtd_metros):
        self.descricao = descricao
        self.qtd_material = qtd_material
        self.valor_mao_de_obra = valor_mao_de_obra
        self.valor_total = valor_total
        self.qtd_metros = qtd_metros


class MaterialServico(db.model):
    __tablename__ = "tbMaterialServico"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_material = db.Column(db.Integer, db.ForeignKey('tbMaterial.id'))
    id_servico = db.Column(db.Integer, db.ForeignKey('tbServico.id'))

    def __init__(self, id_material, id_servico):
        self.id_material = id_material
        self.id_servico = id_servico
