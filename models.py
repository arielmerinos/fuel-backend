import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ValeGasolina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    litros = db.Column(db.Float, nullable=False)
    costo = db.Column(db.Float, nullable=False)
    estacion = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha.isoformat(),
            'litros': self.litros,
            'costo': self.costo,
            'estacion': self.estacion
        }