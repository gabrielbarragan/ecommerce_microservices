from importlib.machinery import SourceFileLoader
import pytest

from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.users.entities.seller import Seller
from src.users.repositories.sqlalchemy_sellers_repository import SQLAlchemySellersRepository

# Tests para el repositorio de libros usando SQLAlchemy, conectándose
# con el contenedor MySQL corriendo con Docker Compose.

# Contiene las mismas pruebas que el repositorio en Firestore. Ver ese archivo
# para ver una explicación de cómo funcionan los fixtures de Pytest.

@pytest.fixture(scope = "session")
def client():
    return SQLAlchemyClient()

@pytest.fixture(scope = "session")
def repository(client):
    return SQLAlchemySellersRepository(client, test = True)

@pytest.fixture(autouse = True)
def before_each(repository):
    
    # Limpiar los libros antes de cada prueba, para no afectar los resultados
    # de las pruebas siguientes.

    repository.hard_delete_all_sellers()
    yield

@pytest.fixture(autouse = True, scope = "session")
def before_and_after_all(client, repository):

    # Crear la tabla antes de todas las pruebas y eliminarla después de todas.

    client.create_tables()
    
    yield
    
    repository.drop_sellers_table()
    client.dispose_mapper()

class TestSqlAlchemySellersRepository:

    def test_create_and_get_seller(self, repository):

        # Agregar al repositorio un libro nuevo.

        id = "1"
        username = "test"
        first_name = "test"
        last_name = "test"
        email = "test"
        password = "test"
        description = "test"
        store_address = "test"
        
        seller = Seller(None, username, first_name, last_name, email, password, description, store_address)
        seller = repository.create_seller(seller)

        print("Created book:", seller.to_dict())

        # Pedir la instancia del libro recién guardado.

        saved_seller = repository.get_seller(seller.id)

        sellers = repository.get_sellers()
        for seller in sellers:
            print(SourceFileLoader)

        print(saved_seller)
        
        print("Saved seller:", saved_seller.to_dict())

        # Afirmar que ambos libros sean iguales.

        assert seller.id == saved_seller.id
        assert seller.username == saved_seller.username
        assert seller.first_name == saved_seller.first_name
        assert seller.last_name == saved_seller.last_name
        assert seller.email == saved_seller.email
        assert seller.password == saved_seller.password
        assert seller.description == saved_seller.description
        assert seller.store_address == saved_seller.store_address

    def test_delete_seller(self, repository):

        # Agregar al repositorio tres libros y guardar sus IDs.

        username = "test"
        email = "test"
        store_address = 30

        ids = []

        for i in range(0, 3):
            seller = Seller(None, username, email, store_address)
            seller = repository.create_seller(seller)
            ids.append(seller.id)

        print("Added seller:", ids)

        # Eliminar el segundo libro del repositorio.

        deleted_id = ids.pop(1)
        print(deleted_id)
        repository.hard_delete_seller(deleted_id)

        print("Deleted seller:", deleted_id)

        # Obtener las IDs de los libros restantes.

        sellers = repository.get_sellers()

        current_ids = []
        for seller in sellers:
            current_ids.append(seller.id)

        print("Current sellers:", current_ids)
        print("Expected sellers:", ids)

        # Afirmar que las IDs restantes correspondan
        # a los recursos que no fueron eliminados.

        assert set(current_ids) == set(ids)
