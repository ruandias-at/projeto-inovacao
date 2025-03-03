from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

    def set_senha(self, senha):
        from werkzeug.security import generate_password_hash
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.senha_hash, senha)

class ContratoFrete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transportadora = db.Column(db.String(100), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('contratos', lazy=True))

    def excluir(self):
        """Exclui o contrato do banco de dados."""
        db.session.delete(self)
        db.session.commit()
