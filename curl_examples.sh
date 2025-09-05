# 1. Obtener todos los grupos
curl -i http://localhost:5000/bands

# 2. Obtener un grupo por ID (ejemplo: 1)
curl -i http://localhost:5000/bands/1

# 3. Obtener un grupo inexistente (ejemplo: 99)
curl -i http://localhost:5000/bands/99

# 4. Crear un nuevo grupo
curl -i -X POST http://localhost:5000/bands \
  -H "Content-Type: application/json" \
  -d '{"name": "The Beatles", "albums": ["Abbey Road", "Sgt. Peppers Lonely Hearts Club Band"]}'

# 5. Crear un grupo con datos incompletos
curl -i -X POST http://localhost:5000/bands \
  -H "Content-Type: application/json" \
  -d '{"name": "Nirvana"}'

# 6. Actualizar un grupo existente (ejemplo: 2)
curl -i -X PUT http://localhost:5000/bands/2 \
  -H "Content-Type: application/json" \
  -d '{"name": "Pink Floyd", "albums": ["Animals", "The Wall"]}'

# 7. Actualizar un grupo inexistente (ejemplo: 99)
curl -i -X PUT http://localhost:5000/bands/99 \
  -H "Content-Type: application/json" \
  -d '{"name": "Unknown", "albums": ["None"]}'

# 8. Eliminar un grupo existente (ejemplo: 3)
curl -i -X DELETE http://localhost:5000/bands/3

# 9. Eliminar un grupo inexistente (ejemplo: 99)
curl -i -X DELETE http://localhost:5000/bands/99

# 10. Crear un grupo con un arreglo vacío de álbumes
curl -i -X POST http://localhost:5000/bands \
  -H "Content-Type: application/json" \
  -d '{"name": "AC/DC", "albums": []}'