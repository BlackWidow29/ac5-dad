from flask import render_template, request, redirect, url_for, make_response, session
from flask_login import login_user, logout_user
from app import app, db
from app.model.User import User
from app.model.MaterialServico import MaterialServico
from app.model.Material import Material
from app.model.Servico import Servico
from app.model.Orcamento import Orcamento
from app.model.Endereco import Endereco
from ast import literal_eval
from sqlalchemy import func
from requests import api


@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/cadastromateriais')
def cadastrar_materiais():
    lista_material = request.cookies.get('materiais')
    if lista_material:
        literal_eval(lista_material)
    else:
        lista_material = {}
        print(len(lista_material))
    return render_template('cadastro_materiais.html', valor_total=0, lista_material=lista_material)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not User or not user.verify_password(password):
            return redirect(url_for('login'))

        #login_user(user)
        session['username'] = user.name
        return redirect(url_for('home'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/servico', methods=['GET', 'POST'])
def servico():
    servico_dic = literal_eval(request.cookies.get('servico'))
    servico = Servico(servico_dic['descricao'], servico_dic['valor_mao_de_obra'], servico_dic['valor_total'])
    lista_material = literal_eval(request.cookies.get('materiais'))
    db.session.add(servico)
    db.session.commit()
    id_servico = db.session.query(func.max(Servico.id))
    for material in lista_material:
        material = Material(lista_material[material]['preco'], lista_material[material]['descricao'],
                            lista_material[material]['tipo'])
        db.session.add(material)
        db.session.commit()
        id_material = db.session.query(func.max(Material.id))
        material_servico = MaterialServico(id_material, id_servico)
        db.session.add(material_servico)
        db.session.commit()
    resp = make_response(redirect('/cadastromateriais'))
    resp.set_cookie('servico', '', expires=0)
    resp.set_cookie('materiais', '', expires=0)
    return resp


@app.route('/adicionarmaterial', methods=['POST'])
def adicionar_material():
    preco = request.form['preco']
    descricao = request.form['descricao']
    tipo = request.form['tipo']

    dic = request.cookies.get('materiais')
    if dic:
        dic = literal_eval(dic)
        key = 'Material' + str(len(dic) + 1)
        dic[key] = {"preco": preco, "descricao": descricao, "tipo": tipo}
        resp = make_response(render_template('cadastro_materiais.html', lista_material=dic, valor_total=0))
        resp.set_cookie('materiais', str(dic))

    else:
        key = 'Material' + str(1)
        dic = {}
        dic[key] = {"preco": preco, "descricao": descricao, "tipo": tipo}
        resp = make_response(render_template('cadastro_materiais.html', lista_material=dic, valor_total=0))
        resp.set_cookie('materiais', str(dic))

    return resp


@app.route('/calcularvalortotal', methods=['POST'])
def calcular_valor_total():
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor_mao_de_obra = request.form['valormaodeobra']
        valor_total = 0
        lista_material = literal_eval(request.cookies.get('materiais'))
        for material in lista_material:
            valor_total += int(lista_material[material]['preco'])

        valor_total += int(valor_mao_de_obra)
        servico = {"descricao": descricao, "valor_mao_de_obra": valor_mao_de_obra, "valor_total": valor_total}
        resp = make_response(
            render_template('cadastro_materiais.html', valor_total=valor_total, lista_material=lista_material))
        resp.set_cookie('servico', str(servico))
        return resp


@app.route('/pegarendereco/<cep>', methods=['POST', 'GET'])
def pegar_endereco(cep):
    dados_endereco = api.get(f"https://viacep.com.br/ws/{cep}/json/unicode/").json()
    return dados_endereco


@app.route('/orcamento', methods=['POST', 'GET'])
def orcamento():
    if request.method == 'POST':
        cep = request.form['cep']
        logradouro = request.form['logradouro']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['uf']
        complemento = request.form['complemento']

        nome_cliente = request.form['nome_cliente']
        observacoes = request.form['observacoes']
        valor_total = request.form['valor_total']
        numero_endereco = request.form['numero_endereco']

        endereco = Endereco.query.filter_by(cep=cep).first()

        if not endereco:
            endereco = Endereco(cep, logradouro, bairro, cidade, estado, complemento)
            db.session.add(endereco)
            db.session.commit()
            endereco = Endereco.query.filter_by(cep=cep).first()

        orcamento = Orcamento(nome_cliente, observacoes, valor_total, numero_endereco, endereco.id)
        db.session.add(orcamento)
        db.session.commit()

        return redirect('/orcamento')

    elif request.method == 'GET':
        return render_template('cadastro_orcamento.html')
