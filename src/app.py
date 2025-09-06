from flask import Flask
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.biciusuario_bd import biciusuario_bp  # corregido nombre
from config.database import engine
from models.Biciusuario import Base  # asegurarse del nombre correcto y minusculas

def create_tables():
    Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.register_blueprint(biciusuario_bp)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0')
