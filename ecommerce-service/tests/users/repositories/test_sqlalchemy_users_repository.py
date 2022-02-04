import pytest, random

from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.users.entities.user import User
from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository

# Tests para el repositorio de usuarios usando SQLAlchemy, conectándose
# con el contenedor MySQL corriendo con Docker Compose.

# Contiene las mismas pruebas que el repositorio en Firestore. Ver ese archivo
# para ver una explicación de cómo funcionan los fixtures de Pytest.

@pytest.fixture(scope = "session")
def client():
    return SQLAlchemyClient()

@pytest.fixture(scope = "session")
def repository(client):
    return SQLAlchemyUsersRepository(client, test = True)

@pytest.fixture(autouse = True)
def before_each(repository):
    
    # Limpiar los libros antes de cada prueba, para no afectar los resultados
    # de las pruebas siguientes.

    repository.hard_delete_all_users()
    yield

@pytest.fixture(autouse = True, scope = "session")
def before_and_after_all(client, repository):

    # Crear la tabla antes de todas las pruebas y eliminarla después de todas.

    client.create_tables()
    
    yield
    
    repository.drop_users_table()
    client.dispose_mapper()

class TestSqlAlchemyUsersRepository:

    def test_create_and_get_user(self, repository):

        # Agregar al repositorio un usuario nuevo.

        username = "test"
        first_name = "test"
        last_name = "test"
        email = "test@test.com"
        password = "password_Test"
        shipping_address = "test #1-23"
        i=random.randint(1,10)
        user = User(None, username, first_name, last_name, f'{i}{email}', password, shipping_address)
        user = repository.create_user(user)

        print("Created user:", user.to_dict())

        # Pedir la instancia del usuario recién guardado.

        saved_user = repository.get_user(user.id)

        users = repository.get_users()
        for user in users:
            print(user)

        print(saved_user)
        
        print("Saved user:", saved_user.to_dict())
        

        # Afirmar que ambos usuarios sean iguales.

        assert user.id          == saved_user.id
        assert user.username    == saved_user.username
        assert user.first_name  == saved_user.first_name
        assert user.last_name   == saved_user.last_name
        assert user.email       == saved_user.email
        assert user.password    == saved_user.password
        assert user.shipping_address  == saved_user.shipping_address

    def test_delete_user(self, repository):

        # Agregar al repositorio tres usuarios y guardar sus IDs.

        username = "test"
        first_name = "test"
        last_name = "test"
        email = "test@tst3.com"
        password = "password_Test"
        shipping_address = "test #1-23"

        ids = []

        for i in range(0, 3):
            user = User(None, f'{i}{username}', first_name, last_name, f'{i}{email}', password, shipping_address)
            user = repository.create_user(user)
            ids.append(user.id)

        print("Added users:", ids)

        # Eliminar el segundo usuario del repositorio.

        deleted_id = ids.pop(1)
        print(deleted_id)
        repository.hard_delete_user(deleted_id)

        print("Deleted user:", deleted_id)

        # Obtener las IDs de los usuarios restantes.

        users = repository.get_users()

        current_ids = []
        for user in users:
            current_ids.append(user.id)

        print("Current usuarios:", current_ids)
        print("Expected usuarios:", ids)

        # Afirmar que las IDs restantes correspondan
        # a los recursos que no fueron eliminados.

        assert set(current_ids) == set(ids)
