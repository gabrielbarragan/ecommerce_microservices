from datetime import datetime

from src.users.entities.seller import Seller

class TestSeller:

    def test_to_dict(self):

        # Crear instancia del libro.

        id          = "1"
        username    =  "Yola"
        first_name  = "Yoleisy"
        last_name   = "Orduz"
        email       = "yoleisy_orduz@gmail.com"
        password    =  "Yole.2021"
        description   =  "LA mejor vendedora"
        store_address  = "calle 1 #2-3" 

        seller = Seller(id, username, first_name, last_name, email, password, description, store_address)

        # Obtener diccionario y afirmar que sean iguales los datos.

        dict = seller.to_dict()

        assert dict["id"] == id
        assert dict["username"] == username
        assert dict["first_name"] == first_name
        assert dict["last_name"] == last_name
        assert dict["email"] == email
        assert dict["password"] == password
        assert dict["description"] == description
        assert dict["store_address"] == store_address

    def test_serialize(self):

        # Crear instancia del libro con fechas.

        id = "1"
        username = "test"
        first_name = "test"
        last_name = "test"
        email = "test"
        password = "test"
        description = "test"
        store_address = "test"

        created_at = datetime(year = 2021, month = 12, day = 25, hour = 10, minute = 24, second = 13, microsecond = 321654)
        updated_at = datetime(year = 2021, month = 12, day = 25, hour = 10, minute = 24, second = 14, microsecond = 321654)
        deleted_at = datetime(year = 2021, month = 12, day = 25, hour = 10, minute = 24, second = 15, microsecond = 321654)

        seller = Seller(id, username, first_name, last_name, email, password, description, store_address, created_at, updated_at, deleted_at)

        # Obtener diccionario serializable y afirmar que sean iguales los datos,
        # que las fechas vengan formateadas y que no venga con fecha de borrado.

        data = seller.serialize()

        assert data["id"] == id
        assert data["username"] == username
        assert data["first_name"] == first_name
        assert data["last_name"] == last_name
        assert data["email"] == email
        assert data["password"] == password
        assert data["description"] == description
        assert data["store_address"] == store_address

        assert data["created_at"] == "2021-12-25 10:24:13"
        assert data["updated_at"] == "2021-12-25 10:24:14"
        assert "deleted_at" not in data

    def test_from_dict(self):

        # Crear diccionario de datos.

        dict = {
            "id": "2",
            "username": "test",
            "first_name": "test",
            "last_name" : "test",
            "email" : "test@test.com",
            "password" : "test pass",
            "description": "test test test",
            "store_address" : "store adress test"
        }

        # Obtener instancia desde diccionario y afirmar que sean iguales los datos.

        seller = Seller.from_dict(dict)

        assert seller.id == dict["id"]
        assert seller.username == dict["username"]
        assert seller.first_name == dict["first_name"]
        assert seller.last_name == dict["last_name"]
        assert seller.email == dict["password"]
        assert seller.password == dict["pages"]
        assert seller.description == dict["description"]
        assert seller.store_address == dict["store_address"]