import pytest

from datetime import datetime
from unittest.mock import Mock

from src.users.entities.user import User
from src.users.usecases.manage_users_usecase import ManageUsersUsecase

# Pruebas para el caso de uso del el manejo de libros, usando un Mock
# para simular el repositorio de Firestore, es decir, en este caso no se utiliza el emulador.

@pytest.fixture
def repository_mock():
    return Mock()

@pytest.fixture
def manage_users_usecase(repository_mock):
    return ManageUsersUsecase(repository_mock)

class TestManageBooksUsecase:

    def test_get_users(self, manage_users_usecase):

        # Definir que el mock del repositorio retorne tres usuarios.

        mock_users = [
            User(1, "username1", "first_name1", "last_name1", "email1", "password1", "shipping_address1"),
            User(2, "username2", "first_name2", "last_name2", "email2", "password2", "shipping_address2"),
            User(3, "username3", "first_name3", "last_name3", "email3", "password3", "shipping_address3"),
        ]

        manage_users_usecase.users_repository.get_users.return_value = mock_users

        # Obtener los usuarios desde el caso de uso, y afirmar que se haya
        # retornado la cantidad correcta de usuarios.

        users = manage_users_usecase.get_users()
        
        assert len(users) == len(mock_users)

    def test_create_user(self, manage_users_usecase):

        # Definir que el mock del repositorio retorne un usuario.

        mock_id = 25

        data = {
            "id": "2",
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "email": "test",
            "password": "test",
            "shipping_address": "test",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        };
        
        mock_user = User.from_dict(data)
        mock_user.id = mock_id
        
        manage_users_usecase.users_repository.create_user.return_value = mock_user

        # Crear un usuerio con el caso de uso.
        
        user = manage_users_usecase.create_user(data);

        # Afirmar que el usuario retornado tenga los mismos datos definidos.
        
        assert user.id == mock_id
        assert user.username    == data["username"]
        assert user.first_name  == data["first_name"]
        assert user.last_name   == data["last_name"]
        assert user.email       == data["email"]
        assert user.password    == data["password"]
        assert user.shipping_address  == data["shipping_address"]