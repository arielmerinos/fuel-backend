from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from models import db, ValeGasolina

# Inicialización de la app 
app = Flask(__name__)

# Configuración de la base de datos
# Aquí puedes configurar la URI de la base de datos, por ejemplo, usando SQLite para desarrollo
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fuel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Inicializar SQLAlchemy y Migrate con la aplicación
db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)



# Importar los modelos (por ejemplo, el modelo de ValeGasolina)
# from models import ValeGasolina

# Rutas de la API
@app.route('/vales', methods=['GET'])
def get_vales():
    # Obtener todos los vales de gasolina de la base de datos
    vales = ValeGasolina.query.all()
    return jsonify({'vales': [vale.to_dict() for vale in vales]})


@app.route('/vale', methods=['POST'])
def create_vale():
    data = request.json

    # Aquí deberías validar los datos...
    # ...
    fecha_dt = datetime.fromisoformat(data['fecha'])

    vale = ValeGasolina(
        fecha=fecha_dt,
        litros=data['litros'],
        costo=data['costo'],
        estacion=data['estacion']
    )

    db.session.add(vale)
    db.session.commit()

    return jsonify({'vale': vale.to_dict()}), 201


@app.route('/vale/<int:vale_id>', methods=['PUT'])
def update_vale(vale_id):
    data = request.json
    vale = ValeGasolina.query.get(vale_id)

    if not vale:
        return jsonify({'message': 'Vale no encontrado'}), 404

    # Actualizar los campos del vale
    vale.fecha = data.get('fecha', vale.fecha)
    vale.litros = data.get('litros', vale.litros)
    vale.costo = data.get('costo', vale.costo)
    vale.estacion = data.get('estacion', vale.estacion)

    db.session.commit()

    return jsonify({'vale': vale.to_dict()})


@app.route('/vale/<int:vale_id>', methods=['DELETE'])
def delete_vale(vale_id):
    # Lógica para eliminar un vale de gasolina
    pass

# Punto de entrada
if __name__ == '__main__':
    # Correr la aplicación en modo desarrollo para facilitar la depuración
    app.run(debug=True)