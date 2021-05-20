from flask import render_template, request, redirect, url_for, make_response
from flask_login import login_user, logout_user
from app import app, db
from app.model.tables import User, Servico, Material, MaterialServico
from json import loads, dumps
from sqlalchemy import func


@app.route('/')
def home():
    return render_template('home.html')


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
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor_mao_de_obra =  request.form['valor_mao_de_obra']
        servico = Servico(descricao, valor_mao_de_obra, 0)
        lista_material = loads(request.cookies.get('materiais'))
        servico = calcularValorTotal(servico, lista_material)
        db.session.add(servico)
        id_servico = Servico.query(func.max(Servico.id))
        db.session.commit()



@app.route('/adicionarmaterial', methods=['POST'])
def adicionar_material():
    preco = request.form['preco']
    descricao = request.form['descricao']
    tipo = request.form['tipo']

    dic = loads(request.cookies.get('materiais'))
    if dic:
        key = 'Material' + str(len(dic))
        dic[key] = {"preco": preco, "descricao": descricao, "tipo": tipo}
        resp = make_response(render_template('cadastro_materiais.html'))
        resp.set_cookie('materiais', dic)

    else:
        key = 'Material' + str(len(dic)+1)
        dic[key] = {"preco": preco, "descricao": descricao, "tipo": tipo}
        resp = make_response(render_template('cadastro_materiais.html'))
        resp.set_cookie('materiais', dic)

    return resp

@app.route('/calcularvalortotal/<servico>/<lista_material>', methods=['GET'])
def calcularValorTotal(servico, lista_material):
    valor_total_material = 0
    for material in lista_material:
        valor_total_material += lista_material[material]['preco']

    servico.valor_total = valor_total_material
    servico.valor_total += servico.valor_mao_de_obra
    resp = make_response(render_template('cadastro_materiais.html'))
    resp.set_cookie('materiais', servico)
