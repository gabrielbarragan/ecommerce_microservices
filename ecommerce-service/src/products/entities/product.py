from src.utils.utils import format_date

# Entidad representando a un usuario.

class Product():

    def __init__(self, id, sku, product_name, description, quantity, seller_id, created_at = None, updated_at = None, deleted_at = None):

        self.id = id
        self.sku = sku
        self.product_name = product_name
        self.description = description
        self.quantity = quantity
        self.seller_id = seller_id
        
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):

        # Transforma los campos de este objeto a un diccionario,
        # útil para guardar contenido en los repositorios.

        return {
            "id": self.id,
            "sku": self.sku,
            "product_name": self.product_name,
            "description": self.description,
            "quantity": self.quantity,
            "seller": self.seller_id,
            
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    def serialize(self):

        # Retorna un diccionario serializable a JSON.
        # Es parecido a "to_dict", pero es útil para mostrar datos en el exterior,
        # como por ejemplo retornar una respuesta hacia al usuario desde el endpoint.
        # En este caso no se retorna la fecha "deleted_at", ya que es información
        # privada, y las fechas se transforman a un formato legible.

        data = self.to_dict()
        
        data.pop("deleted_at")
        
        data["created_at"] = format_date(data["created_at"])
        data["updated_at"] = format_date(data["updated_at"])

        return data

    @classmethod
    def from_dict(cls, dict):

        id = dict.get("id")
        sku = dict.get("sku")
        product_name = dict.get("product_name")
        description = dict.get("description")
        quantity = dict.get("quantity")
        seller_id = dict.get("seller_id")

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return Product(id, sku, product_name, description, quantity, seller_id, created_at, updated_at, deleted_at)
