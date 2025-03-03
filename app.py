from flask import Flask, render_template, request, redirect, url_for
from models import db, ContratoFrete

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ruan@localhost:5432/proj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def dashboard():
    contratos = ContratoFrete.query.all()
    return render_template('dashboard.html', contratos=contratos)

@app.route('/novo_contrato', methods=['GET', 'POST'])
def novo_contrato():
    if request.method == 'POST':
        # Coletar dados do formulário e criar um novo contrato
        transportadora = request.form['transportadora']
        cliente = request.form['cliente']
        valor = request.form['valor']
        novo_contrato = ContratoFrete(transportadora=transportadora, cliente=cliente, valor=valor)
        db.session.add(novo_contrato)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('novo_contrato.html')

@app.route('/contrato/<int:id>')
def contrato(id):
    contrato = ContratoFrete.query.get_or_404(id)
    return render_template('contrato.html', contrato=contrato)

if __name__ == '__main__':
    app.run(debug=True)
