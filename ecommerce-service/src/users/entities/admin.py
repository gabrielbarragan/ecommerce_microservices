from src.utils.utils import format_date
from src.users.entities.user import User
# Entidad representando a un usuario.


class Admin(User):
    """Admin class hereda de la clase User en este caso no tiene el 
    campo shipping address"""

    def __init__(self, id, username, first_name, last_name, email, password, created_at = None, updated_at = None, deleted_at = None):

        super().__init__(id, username, first_name, last_name, email, password,created_at, updated_at, deleted_at)


    def to_dict(self):

        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
    @classmethod
    def from_dict(cls, dict):

        id = dict.get("id")
        username = dict.get("username")
        first_name = dict.get("first_name")
        last_name = dict.get("last_name")
        email = dict.get("email")
        password = dict.get("password")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return Admin(id, username, first_name, last_name, email, password, created_at, updated_at, deleted_at)