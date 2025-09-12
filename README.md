# Proyecto de gestión de Biciusuarios.
Este proyecto es una base para la gestión de biciusuarios, sus registros y bicicletas, implementado siguiendo el patrón arquitectónico por capas.
Utiliza Python, Flask como framework web y SQLAlchemy como ORM para la interacción con bases de datos relacionales.

## Descripción general 📖
El sistema permite:Registrar nuevos biciusuarios,consultar información detallada de cada usuario, actualizar sus datos(incluyendo registros y bicicletas asociadas) y eliminar usuarios junto con toda la información relacionada.

La arquitectura por capas facilita la separación de responsabilidades, mejorando la mantenibilidad, escalabilidad y flexibilidad del código.
El uso de un ORM como SQLAlchemy permite desacoplar la lógica de negocio de la base de datos, facilitando la portabilidad y seguridad.

### Caracteristicas principales
- API RESTful para la gestión de biciusuarios, registros y bicicletas.
- Modelos bien definidos con relaciones entre entidades (Biciusuario, RegistroBiciusuario, Bicicleta).
- Servicios dedicados para la lógica de negocio (CRUD completo).
- Controladores que exponen los endpoints de la API.
- Cascada en eliminaciones → al borrar un usuario, se eliminan automáticamente sus registros y bicicletas.
- Uso de joinedload en consultas para optimizar la carga de relaciones.

## Estructura del proyecto📂 
- `models/`: Definición de los modelos de datos (`Biciusuario`, `RegistroBiciusuario`, `Bicicleta`) y sus relaciones.
- `services/`: Implementación de la lógica de negocio y acceso a datos usando SQLAlchemy (CRUD de biciusuarios, registros y bicicletas).
- `controllers/`: Definición de los endpoints y controladores de la API REST (usa Flask Blueprints para organizar rutas).
- `config/`: Configuración de la base de datos (`database.py`) con soporte para MySQL y fallback a SQLite.
- `app.py`: Punto de entrada de la aplicación Flask. Registra los blueprints y crea las tablas si no existen.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.

## Tecnologias utilizadas
- Python 3.12+
- Flask (framework web)
- SQLAlchemy (ORM para bases de datos relacionales)
- SQLite / MySQL (soporte de motores de BD)
- dotenv para configuración de entornos

## Cómo crear un entorno virtual en Python
El uso de un entorno virtual es fundamental para aislar las dependencias del proyecto y evitar conflictos con otras aplicaciones o proyectos en tu sistema. Un entorno virtual te permite instalar paquetes específicos para este proyecto sin afectar el entorno global de Python.

### Pasos para crear y activar un entorno virtual:

1. **Instala virtualenv si no lo tienes:**
   ```bash
   pip install virtualenv
   ```

2. **Crea el entorno virtual:**
   ```bash
   python -m venv venv
   ```
   Esto creará una carpeta llamada `venv` en el directorio del proyecto.

3. **Activa el entorno virtual:**
   - En Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - En Windows:
     ```cmd
     venv\Scripts\activate
     ```

4. **Instala las dependencias del proyecto:**
   ```bash
   pip install -r requirements.txt
   ```

### Importancia de usar un entorno virtual
- **Aislamiento:** Evita conflictos entre dependencias de diferentes proyectos.
- **Reproducibilidad:** Permite que otros desarrolladores instalen exactamente las mismas versiones de las librerías.
- **Facilidad de despliegue:** Simplifica la migración y despliegue en diferentes entornos (desarrollo, pruebas, producción).
- **Limpieza:** Mantiene tu instalación global de Python libre de paquetes innecesarios.

### Ejecuta la aplicación con:
python app.py

### La API estará disponible en:
http://localhost:5000



## Contribuciones
Si deseas contribuir, por favor sigue las buenas prácticas de documentación y arquitectura ya establecidas en el proyecto. ¡Toda mejora es bienvenida!

## Licencia
Este proyecto es de uso libre para fines educativos y de aprendizaje.
