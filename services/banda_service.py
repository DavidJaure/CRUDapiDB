from config.database import SessionLocal
from models.band import Band, Album
from sqlalchemy.orm import joinedload

def get_all_bands():
    session = SessionLocal()
    bands = session.query(Band).options(joinedload(Band.albums)).all()
    result = []
    for band in bands:
        result.append({
            'id': band.id,
            'name': band.name,
            'albums': [album.title for album in band.albums]
        })
    session.close()
    return result

def get_band_by_id(band_id):
    session = SessionLocal()
    band = session.query(Band).options(joinedload(Band.albums)).filter(Band.id == band_id).first()
    if band:
        result = {
            'id': band.id,
            'name': band.name,
            'albums': [album.title for album in band.albums]
        }
    else:
        result = None
    session.close()
    return result

def create_band(data):
    session = SessionLocal()
    band = Band(name=data['name'])
    session.add(band)
    session.commit()
    for album_title in data.get('albums', []):
        album = Album(title=album_title, band_id=band.id)
        session.add(album)
    session.commit()
    result = {
        'id': band.id,
        'name': band.name,
        'albums': [album.title for album in band.albums]
    }
    session.close()
    return result

def update_band(band_id, data):
    session = SessionLocal()
    band = session.query(Band).filter(Band.id == band_id).first()
    if not band:
        session.close()
        return None
    band.name = data.get('name', band.name)
    if 'albums' in data:
        band.albums.clear()
        for album_title in data['albums']:
            album = Album(title=album_title, band_id=band.id)
            band.albums.append(album)
    session.commit()
    result = {
        'id': band.id,
        'name': band.name,
        'albums': [album.title for album in band.albums]
    }
    session.close()
    return result

def delete_band(band_id):
    session = SessionLocal()
    band = session.query(Band).filter(Band.id == band_id).first()
    if not band:
        session.close()
        return False
    session.delete(band)
    session.commit()
    session.close()
    return True