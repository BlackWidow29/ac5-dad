from flask import render_template, request, redirect, url_for, make_response
from flask_login import login_user, logout_user
from app import app, db
from app.model.tables import User, Servico, Material, MaterialServico
from ast import literal_eval
from sqlalchemy import func


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/cadastromateriais')
def cadastrar_materiais():
    lista_material = request.cookies.get('materiais')
    if lista_material:
        literal_eval(lista_material)
    else:
        lista_material = {}
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

        login_user(user)
        return redirect(url_for('home'))

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
        resp = make_response(render_template('cadastro_materiais.html', valor_total=valor_total, lista_material=lista_material))
        resp.set_cookie('servico', str(servico))
        return resp
