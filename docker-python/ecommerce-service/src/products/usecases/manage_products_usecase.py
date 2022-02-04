from src.products.entities.product import Product
from src.utils import utils

# Casos de uso para el manejo de usuarios.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.

class ManageProductsUsecase:

    def __init__(self, products_repository):
        self.products_repository = products_repository

    def get_all_products(self):

        # Retorna una lista de entidades User desde el repositorio.

        return self.products_repository.get_all_products()

    def get_products(self, seller_id):

        # Retorna una lista de entidades seller desde el repositorio.

        return self.products_repository.get_products(seller_id)
    def get_product(self, seller_id, product_sku):

        # Retorna una lista de entidades seller desde el repositorio.

        return self.products_repository.get_product(seller_id, product_sku)
    

    def create_product(self, data, seller_id):

        # Crea una instancia User desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
            
        current_time = utils.get_current_datetime()
        
        data["created_at"] = current_time
        data["updated_at"] = current_time
        data["seller_id"]  = seller_id

        product = Product.from_dict(data)
        product = self.products_repository.create_product(product)

        return product
    
    def update_product(self, seller_id, product_sku, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        product = self.get_product(seller_id, product_sku)

        if product:

            data["updated_at"] = utils.get_current_datetime()
            product = self.products_repository.update_product(seller_id, product_sku, data)

            return product

        else:
            raise ValueError(f"Product of ID {product_sku} for Seller {seller_id} doesn't exist.")

    def delete_product(self, product_sku, seller_id, ):

        # Realiza un soft-delete del producto con la ID especificada y el sku de producto indicado, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".
        
        user = self.get_product(seller_id, product_sku)

        if user:

            data = {
                "deleted_at": utils.get_current_datetime()
            }
            
            user = self.products_repository.update_product(seller_id, product_sku, data)

        else:
            raise ValueError(f"Product of ID {product_sku} for seller {seller_id} doesn't exist or is already deleted.")