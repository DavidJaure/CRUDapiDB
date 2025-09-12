from config.database import SessionLocal
from models.Biciusuario import Biciusuario, RegistroBiciusuario, Bicicleta
from sqlalchemy.orm import joinedload

def get_all_biciusuarios():
    session = SessionLocal()
    biciusuarios = session.query(Biciusuario).options(
        joinedload(Biciusuario.registros),
        joinedload(Biciusuario.bicicletas)
    ).all()
    result = []
    for user in biciusuarios:
        result.append({
            'id': user.id,
            'nombre_biciusuario': user.nombre_biciusuario,
            'registros': [{'id': r.id, 'serial': r.serial} for r in user.registros],
            'bicicletas': [{
                'id': b.id,
                'marca': b.marca,
                'modelo': b.modelo,
                'color': b.color,
                'serial': b.serial
            } for b in user.bicicletas]
        })
    session.close()
    return result

def get_biciusuario_by_id(biciusuario_id):
    session = SessionLocal()
    user = session.query(Biciusuario).options(
        joinedload(Biciusuario.registros),
        joinedload(Biciusuario.bicicletas)
    ).filter(Biciusuario.id == biciusuario_id).first()
    if user:
        result = {
            'id': user.id,
            'nombre_biciusuario': user.nombre_biciusuario,
            'registros': [{'id': r.id, 'serial': r.serial} for r in user.registros],
            'bicicletas': [{
                'id': b.id,
                'marca': b.marca,
                'modelo': b.modelo,
                'color': b.color,
                'serial': b.serial
            } for b in user.bicicletas]
        }
    else:
        result = None
    session.close()
    return result

def create_biciusuario(data):
    session = SessionLocal()
    user = Biciusuario(nombre_biciusuario=data['nombre_biciusuario'])
    session.add(user)
    session.commit()

    # Crear registros asociados si vienen en data
    for reg_data in data.get('registros', []):
        registro = RegistroBiciusuario(
            nombre_biciusuario=user.nombre_biciusuario,
            serial=reg_data['serial'],
            biciusuario_id=user.id
        )
        session.add(registro)

    # Crear bicicletas asociadas si vienen en data
    for bici_data in data.get('bicicletas', []):
        bicicleta = Bicicleta(
            marca=bici_data['marca'],
            modelo=bici_data['modelo'],
            color=bici_data['color'],
            serial=bici_data['serial'],
            biciusuario_id=user.id
        )
        session.add(bicicleta)

    session.commit()

    # Recargar para devolver con relaciones
    session.refresh(user)
    result = get_biciusuario_by_id(user.id)
    session.close()
    return result

def update_biciusuario(biciusuario_id, data):
    session = SessionLocal()
    user = session.query(Biciusuario).filter(Biciusuario.id == biciusuario_id).first()
    if not user:
        session.close()
        return None

    # Actualizar nombre
    user.nombre_biciusuario = data.get('nombre_biciusuario', user.nombre_biciusuario)

    # Actualizar registros
    if 'registros' in data:
        for reg_data in data['registros']:
            registro = next((r for r in user.registros if r.serial == reg_data['serial']), None)
            if registro:
                registro.nombre_biciusuario = user.nombre_biciusuario
            else:
                new_registro = RegistroBiciusuario(
                    nombre_biciusuario=user.nombre_biciusuario,
                    serial=reg_data['serial'],
                    biciusuario_id=user.id
                )
                session.add(new_registro)

    # Actualizar bicicletas
    if 'bicicletas' in data:
        for bici_data in data['bicicletas']:
            bicicleta = next((b for b in user.bicicletas if b.serial == bici_data['serial']), None)
            if bicicleta:
                bicicleta.marca = bici_data.get('marca', bicicleta.marca)
                bicicleta.modelo = bici_data.get('modelo', bicicleta.modelo)
                bicicleta.color = bici_data.get('color', bicicleta.color)
            else:
                new_bici = Bicicleta(
                    marca=bici_data['marca'],
                    modelo=bici_data['modelo'],
                    color=bici_data['color'],
                    serial=bici_data['serial'],
                    biciusuario_id=user.id
                )
                session.add(new_bici)

    session.commit()
    result = get_biciusuario_by_id(user.id)
    session.close()
    return result

def delete_biciusuario(biciusuario_id):
    session = SessionLocal()
    user = session.query(Biciusuario).filter(Biciusuario.id == biciusuario_id).first()
    if not user:
        session.close()
        return False
    session.delete(user)
    session.commit()
    session.close()
    return True
