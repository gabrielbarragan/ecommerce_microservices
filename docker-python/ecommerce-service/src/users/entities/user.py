from src.utils.utils import format_date

# Entidad representando a un usuario.

class User():

    def __init__(self, id, username, first_name, last_name, email, password, shipping_address, created_at = None, updated_at = None, deleted_at = None):

        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.shipping_address = shipping_address
        
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

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
            "shipping_address": self.shipping_address,
            
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    def serialize(self):

        # Retorna un diccionario serializable a JSON.
        # Es parecido a "to_dict", pero es útil para mostrar datos en el exterior,
        # como por ejemplo retornar una respuesta hacia al usuario desde el endpoint.
        # En este caso no se retorna la fecha "deleted_at", ya que es información
        # privada, y las fechas se transforman a un formato legible.

        data = self.to_dict()
        
        data.pop("deleted_at")
        
        data["created_at"] = format_date(data["created_at"])
        data["updated_at"] = format_date(data["updated_at"])

        return data

    @classmethod
    def from_dict(cls, dict):

        id = dict.get("id")
        username = dict.get("username")
        first_name = dict.get("first_name")
        last_name = dict.get("last_name")
        email = dict.get("email")
        password = dict.get("password")
        shipping_address = dict.get("shipping_address")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return User(id, username, first_name, last_name, email, password, shipping_address, created_at, updated_at, deleted_at)

class Seller(User):
    """Seller class hereda de la clase User en este caso no tiene el 
    campo shipping address y se le agregan los campos description y store_address"""

    def __init__(self, id, username, first_name, last_name, email, password, description, store_address, created_at = None, updated_at = None, deleted_at = None):

        super().__init__(id, username, first_name, last_name, email, password,created_at, updated_at, deleted_at)
        self.description = description
        self.store_address= store_address

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
            "description": self.description,
            "store_address": self.store_address,
            
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
        description = dict.get("description")
        store_address = dict.get("store_address")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return Seller(id, username, first_name, last_name, email, password, store_address, description, created_at, updated_at, deleted_at)

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