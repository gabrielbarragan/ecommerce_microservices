from src.frameworks.db.firestore import create_firestore_client
from src.frameworks.db.redis import create_redis_client
from src.frameworks.db.sqlalchemy import SQLAlchemyClient
from src.frameworks.http.flask import create_flask_app



#users
from src.users.http.users_blueprint import create_users_blueprint
from src.users.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository
from src.users.usecases.manage_users_usecase import ManageUsersUsecase

#sellers
from src.users.http.sellers_blueprint import create_sellers_blueprint
from src.users.repositories.sqlalchemy_sellers_repository import SQLAlchemySellersRepository
from src.users.usecases.manage_sellers_usecase import ManageSellersUsecase

#products
from src.products.http.products_blueprint import create_products_blueprint
from src.products.repositories.sqlalchemy_products_repository import SQLAlchemyProductsRepository
from src.products.usecases.manage_products_usecase import ManageProductsUsecase

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

sqlalchemy_client = SQLAlchemyClient()


#users
sqlalchemy_users_repository = SQLAlchemyUsersRepository(sqlalchemy_client)
sqlalchemy_client.create_tables()

#sellers
sqlalchemy_sellers_repository = SQLAlchemySellersRepository(sqlalchemy_client)
sqlalchemy_client.create_tables()

#products
sqlalchemy_products_repository = SQLAlchemyProductsRepository(sqlalchemy_client)
sqlalchemy_client.create_tables()

greeting_usecase = GreetingUsecase(redis_greeting_cache)


manage_users_usecase = ManageUsersUsecase(sqlalchemy_users_repository)
manage_sellers_usecase = ManageSellersUsecase(sqlalchemy_sellers_repository)
manage_products_usecase = ManageProductsUsecase(sqlalchemy_products_repository)

blueprints = [
    create_users_blueprint(manage_users_usecase),
    create_sellers_blueprint(manage_sellers_usecase),
    create_products_blueprint(manage_products_usecase),
    create_greeting_blueprint(greeting_usecase),
]

# Crear aplicación HTTP con dependencias inyectadas.

app = create_flask_app(blueprints)