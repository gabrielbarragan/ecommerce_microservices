from src.frameworks.db.firestore import create_firestore_client
from src.frameworks.db.redis import create_redis_client
from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.frameworks.http.flask import create_flask_app

#books
from src.books.http.books_blueprint import create_books_blueprint
from src.books.repositories.firestore_books_repository import FirestoreBooksRepository
from src.books.repositories.sqlalchemy_books_repository import SQLAlchemyBooksRepository
from src.books.usecases.manage_books_usecase import ManageBooksUsecase

#users
from src.users.http.users_blueprint import create_users_blueprint
from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository
from src.users.usecases.manage_users_usecase import ManageUsersUsecase

#sellers
from src.users.http.sellers_blueprint import create_sellers_blueprint
from src.users.repositories.sqlalchemy_sellers_repository import SQLAlchemySellersRepository
from src.users.usecases.manage_sellers_usecase import ManageSellersUsecase

from src.greeting.http.greeting_blueprint import create_greeting_blueprint
from src.greeting.repositories.redis_greeting_cache import RedisGreetingCache
from src.greeting.usecases.greeting_usecase import GreetingUsecase

# Instanciar dependencias.

# En el caso de uso de de libros, es es posible pasarle como parámetro el repositorio
# de Firestore o el repositorio con SQL Alchemy, y en ambos casos debería funcionar,
# incluso si el cambio se hace mientras la aplicación está en ejecución.

redis_client = create_redis_client()
redis_greeting_cache = RedisGreetingCache(redis_client)

firestore_client = create_firestore_client()
firestore_books_repository = FirestoreBooksRepository(firestore_client)

sqlalchemy_client = SQLAlchemyClient()
sqlalchemy_books_repository = SQLAlchemyBooksRepository(sqlalchemy_client)
sqlalchemy_client.create_tables()

#users
sqlalchemy_users_repository = SQLAlchemyUsersRepository(sqlalchemy_client)
sqlalchemy_client.create_tables()

#sellers
sqlalchemy_sellers_repository = SQLAlchemySellersRepository(sqlalchemy_client)
sqlalchemy_client.create_tables()

greeting_usecase = GreetingUsecase(redis_greeting_cache)
# manage_books_usecase = ManageBooksUsecase(firestore_books_repository)
manage_books_usecase = ManageBooksUsecase(sqlalchemy_books_repository)
manage_users_usecase = ManageUsersUsecase(sqlalchemy_users_repository)
manage_sellers_usecase = ManageSellersUsecase(sqlalchemy_sellers_repository)

blueprints = [
    create_books_blueprint(manage_books_usecase),
    create_users_blueprint(manage_users_usecase),
    create_sellers_blueprint(manage_sellers_usecase),
    create_greeting_blueprint(greeting_usecase),
]

# Crear aplicación HTTP con dependencias inyectadas.

app = create_flask_app(blueprints)