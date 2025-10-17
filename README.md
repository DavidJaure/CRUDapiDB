# Proyecto de Gestión de Registros de Biciusuarios

Este proyecto es una API RESTful diseñada para la administración integral de perfiles de biciusuarios, sus registros de uso y la gestión de bicicletas asociadas. Está implementado siguiendo el riguroso **patrón arquitectónico por capas** (Controller, Service, Repository) y utiliza Python, Flask, y SQLAlchemy.

## Descripción General
El sistema centraliza la información de los usuarios que utilizan bicicletas, proporcionando una plataforma segura para la gestión de datos. La arquitectura por capas garantiza la **separación de responsabilidades**, lo que facilita la mantenibilidad, el *testing* y la futura escalabilidad.

### Características Clave:
- **Autenticación Segura (JWT):** Todas las rutas de gestión de perfiles están protegidas y requieren un **JSON Web Token (JWT)** válido.
- **Seguridad de Contraseñas:** Uso de *hashing* con `werkzeug.security` para almacenar contraseñas de forma segura (campo `password_hash`).
- **Arquitectura por Capas:** Clara distinción entre la capa de acceso a datos (Repository), la lógica de negocio (Service) y la gestión de peticiones HTTP (Controller).
- **Entidades Relacionadas:** Manejo de relaciones uno-a-muchos (`User` -> `RegistroBiciusuario` y `User` -> `Bicicleta`).

## Estructura del Proyecto
- `models/`: Definición de los modelos de datos (User, RegistroBiciusuario, Bicicleta).
- `repositories/`: Implementación de la capa de acceso a datos (`UsersRepository`, `BiciusuariosRepository`).
- `services/`: Implementación de la lógica de negocio (`UsersService` para autenticación y `BiciusuariosService` para perfiles).
- `controllers/`: (Por implementar) Lógica de los endpoints de la API (`users_controllers.py` para login/registro y `biciusuarios_bd.py` para el CRUD principal).
- `requirements.txt`: Lista de dependencias necesarias.

## Requisitos y Configuración Inicial

El uso de un entorno virtual (`venv`) es obligatorio para aislar las dependencias del proyecto.

### Pasos de Configuración:

1.  **Instalar virtualenv (si no lo tienes):**
    ```bash
    pip install virtualenv
    ```

2.  **Crear y Activar el Entorno Virtual:**
    ```bash
    python -m venv venv
    # En Linux/Mac:
    source venv/bin/activate
    # En Windows:
    venv\Scripts\activate
    ```

3.  **Instalar Dependencias del Proyecto:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Correr API**
    ```bash
    python -m src.app
    ```

### Dependencias Críticas (Asegúrate de que estén en `requirements.txt`):
- `Flask`
- `Flask-JWT-Extended`
- `SQLAlchemy`
- `psycopg2-binary` (o el driver de tu base de datos)
- `werkzeug` (para `generate_password_hash`)

## Rutas Principales de la API (Ejemplos)

| Ruta | Método | Descripción | Requisito |
| :--- | :--- | :--- | :--- |
| `/auth/register` | `POST` | Crea un nuevo biciusuario y hashea la contraseña. | Ninguno |
| `/auth/login` | `POST` | Autentica al usuario y retorna un token JWT. | Ninguno |
| `/biciusuarios` | `GET` | Lista todos los perfiles de biciusuario. | **JWT** |
| `/biciusuarios/<id>` | `GET` | Obtiene un perfil específico con sus bicicletas y registros. | **JWT** |
| `/biciusuarios/<id>` | `PUT`/`PATCH`| Actualiza datos del perfil, bicicletas y registros. | **JWT** |
| `/biciusuarios/<id>` | `DELETE` | Elimina un perfil completo. | **JWT** |

## Contribuciones
Si deseas contribuir o proponer mejoras, por favor mantente alineado con la arquitectura por capas (Controller -> Service -> Repository) y las buenas prácticas de seguridad establecidas.

## Licencia
Este proyecto es de uso libre para fines educativos y de aprendizaje.