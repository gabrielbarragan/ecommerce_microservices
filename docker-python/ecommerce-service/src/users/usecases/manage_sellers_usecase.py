from src.users.entities.seller import Seller
from src.utils import utils

# Casos de uso para el manejo de usuarios.

# Recibe en el constructor el repositorio a utilizar. Da igual si recibe el repositorio
# de SQL o de Firestore, el caso de uso debe funcionar independientemente de su implementación.

class ManageSellersUsecase:

    def __init__(self, sellers_repository):
        self.sellers_repository = sellers_repository

    def get_sellers(self):

        # Retorna una lista de entidades User desde el repositorio.

        return self.sellers_repository.get_sellers()

    def get_seller(self, seller_id):

        # Retorna una instancia de User según la ID recibida.

        return self.sellers_repository.get_seller(seller_id)

    def create_seller(self, data):

        # Crea una instancia seller desde la data recibida, que ya debe venir validada desde afuera,
        # y guarda dicha instancia en el repositorio para finalmente retornarla.
            
        current_time = utils.get_current_datetime()
        
        data["created_at"] = current_time
        data["updated_at"] = current_time

        seller = Seller.from_dict(data)
        seller = self.sellers_repository.create_seller(seller,data["email"])

        return seller

    def update_seller(self, seller_id, data):

        # Actualiza los datos recibidos y los guarda en el repositorio según la ID recibida.
        # La data no necesariamente debe contener todos los campos de la entidad, sólo
        # los campos que se van a actualizar. Esta data debe venir validada desde afuera.

        seller = self.get_seller(seller_id)

        if seller:

            data["updated_at"] = utils.get_current_datetime()
            seller = self.sellers_repository.update_seller(seller_id, data)

            return seller

        else:
            raise ValueError(f"Seller of ID {seller_id} doesn't exist.")

    def delete_seller(self, seller_id):

        # Realiza un soft-delete del libro con la ID especificada, si es que existe.
        # A nivel de repositorio realiza una actualización al campo "deleted_at".

        seller = self.get_seller(seller_id)

        if seller:

            data = {
                "deleted_at": utils.get_current_datetime()
            }
            
            seller = self.sellers_repository.update_seller(seller_id, data)

        else:
            raise ValueError(f"Seller of ID {seller_id} doesn't exist or is already deleted.")