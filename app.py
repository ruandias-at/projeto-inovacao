from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Usuario, ContratoFrete  # Importando os modelos corretamente

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ruan@localhost/proj'
app.config['SECRET_KEY'] = 'chave_secreta'

db.init_app(app)  # Inicializa a conexão do banco de dados com o app Flask

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'error')
            return redirect(url_for('cadastro'))

        novo_usuario = Usuario(nome=nome, email=email)
        novo_usuario.set_senha(senha)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            return redirect(url_for('dashboard'))
        else:
            flash('E-mail ou senha incorretos!', 'error')

    return render_template('login.html')

@app.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form['email']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            flash('Se este e-mail estiver cadastrado, você receberá instruções para redefinir sua senha.', 'success')
        else:
            flash('E-mail não encontrado!', 'error')

        return redirect(url_for('login'))

    return render_template('recuperar_senha.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    contratos = ContratoFrete.query.filter_by(usuario_id=current_user.id).all()
    return render_template('dashboard.html', contratos=contratos)

@app.route('/novo_contrato', methods=['GET', 'POST'])
@login_required
def novo_contrato():
    if request.method == 'POST':
        transportadora = request.form['transportadora']
        cliente = request.form['cliente']
        valor = request.form['valor']

        novo_contrato = ContratoFrete(
            transportadora=transportadora,
            cliente=cliente,
            valor=valor,
            usuario_id=current_user.id
        )
        db.session.add(novo_contrato)
        db.session.commit()

        flash('Contrato cadastrado com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('novo_contrato.html')

@app.route('/excluir_contrato/<int:contrato_id>', methods=['POST'])
@login_required
def excluir_contrato(contrato_id):
    contrato = ContratoFrete.query.get_or_404(contrato_id)

    if contrato.usuario_id != current_user.id:
        flash("Você não tem permissão para excluir este contrato.", "error")
        return redirect(url_for('dashboard'))

    contrato.excluir()
    flash("Contrato excluído com sucesso!", "success")
    return redirect(url_for('dashboard'))

@app.route('/contrato/<int:id>')
@login_required
def contrato(id):
    contrato = ContratoFrete.query.get_or_404(id)
    return render_template('contrato.html', contrato=contrato)

if __name__ == '__main__':
    app.run(debug=True)
