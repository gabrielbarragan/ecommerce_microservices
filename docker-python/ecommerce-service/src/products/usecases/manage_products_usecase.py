from src.products.entities.product import Product
from src.utils import utils

# Casos de uso para el manejo de usuarios.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.

class ManageProductsUsecase:

    def __init__(self, products_repository):
        self.products_repository = products_repository

    def get_products(self, seller_id):

        # Retorna una lista de entidades User desde el repositorio.

        return self.products_repository.get_products(seller_id)
    
    def get_all_products(self):

        # Retorna una lista de entidades User desde el repositorio.

        return self.products_repository.get_all_products()

    