from datetime import datetime

from src.users.entities.user import User

class TestUser:

    def test_to_dict(self):

        # Crear instancia del usuario.

        id = "1"
        username = "test"
        first_name = "test"
        last_name = "test"
        email = "test@test1.com"
        password = "password_Test"
        shipping_address = "test #1-23"

        user = User(id, username, first_name, last_name, email, password, shipping_address)

        # Obtener usuario y afirmar que sean iguales los datos.

        dict = user.to_dict()

        assert dict["id"]
        assert dict["username"]
        assert dict["first_name"]
        assert dict["last_name"]
        assert dict["email"]
        assert dict["password"]
        assert dict["shipping_address"]

    def test_serialize(self):

        """Create user instance with dates"""

        id = "2"
        username = "test"
        first_name = "test"
        last_name = "test"
        email = "test@test2.com"
        password = "password_Test"
        shipping_address = "test #1-23"
        created_at = datetime(year = 2021, month = 12, day = 25, hour = 10, minute = 24, second = 13, microsecond = 321654)
        updated_at = datetime(year = 2021, month = 12, day = 25, hour = 10, minute = 24, second = 14, microsecond = 321654)
        deleted_at = datetime(year = 2021, month = 12, day = 25, hour = 10, minute = 24, second = 15, microsecond = 321654)

        user = User(id, username, first_name, last_name, email, password, shipping_address, created_at, updated_at, deleted_at)

        # Obtener diccionario serializable y afirmar que sean iguales los datos,
        # que las fechas vengan formateadas y que no venga con fecha de borrado.

        data = user.serialize()

        assert data["id"]
        assert data["username"]
        assert data["first_name"]
        assert data["last_name"]
        assert data["email"]
        assert data["password"]
        assert data["shipping_address"]
        assert data["created_at"] == "2021-12-25 10:24:13"
        assert data["updated_at"] == "2021-12-25 10:24:14"
        assert "deleted_at" not in data

    def test_from_dict(self):

        # Crear diccionario de datos.

        dict = {
        "id": "2",
        "username": "test",
        "first_name": "test",
        "last_name": "test",
        "email": "test",
        "password": "test",
        "shipping_address": "test",
        }

        # Obtener instancia desde diccionario y afirmar que sean iguales los datos.

        user = User.from_dict(dict)

        assert user.id == dict["id"]  == dict["id"]
        assert user.username    == dict["username"]
        assert user.first_name   == dict["first_name"]
        assert user.last_name   == dict["last_name"]
        assert user.email   == dict["email"]
        assert user.password   == dict["password"]
        assert user.shipping_address   == dict["shipping_address"]