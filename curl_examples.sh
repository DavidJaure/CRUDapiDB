#Mostrar todos los biciusuarios
curl -i http://localhost:5000/biciusuarios

#Mostrar biciusuario por id
curl -i http://localhost:5000/biciusuarios/1

#Mostrar biciusuario por id que no existe
curl -i http://localhost:5000/biciusuarios/99

#Crear biciusuario con registros y bicicletas
curl -i -X POST http://localhost:5000/biciusuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_biciusuario": "Carlos Pérez",
    "registros": [{"serial": "REG123"}],
    "bicicletas": [
      {"marca": "Trek", "modelo": "Domane", "color": "Rojo", "serial": "TREK-001"},
      {"marca": "Giant", "modelo": "Escape", "color": "Azul", "serial": "GIANT-777"}
    ]
  }'

#Crear biciusuario con solo nombre
curl -i -X POST http://localhost:5000/biciusuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre_biciusuario": "Natalia"}'

#Actualizar biciusuario existente 
curl -i -X PUT http://localhost:5000/biciusuarios/2 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_biciusuario": "Carlos Gómez",
    "registros": [{"serial": "REG999"}],
    "bicicletas": [
      {"marca": "Specialized", "modelo": "Sirrus", "color": "Negro", "serial": "SPEC-2025"}
    ]
  }'

#Actualizar biciusuario que no existe
curl -i -X PUT http://localhost:5000/biciusuarios/99 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_biciusuario": "Fantasma",
    "registros": [],
    "bicicletas": []
  }'

#Eliminar biciusuario por id
curl -i -X DELETE http://localhost:5000/biciusuarios/3

#Eliminar biciusuario que no existe
curl -i -X DELETE http://localhost:5000/biciusuarios/99

#Crear biciusuario con listas vacías
curl -i -X POST http://localhost:5000/biciusuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre_biciusuario": "Andrea", "registros": [], "bicicletas": []}'
