from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP, or_
from sqlalchemy.orm import relationship

from src.products.entities.product import Product
from src.users.entities.seller import Seller

    
# Implementación con SQL Alchemy para el repositorio de productos.


class SQLAlchemyProductsRepository():

    def __init__(self, sqlalchemy_client, test = False):

        # Mapear la tabla Product de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Products"

        if test:
            table_name += "_test"

        self.products_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key = True),
            Column("sku", String(50), unique=True),
            Column("product_name", String(50)),
            Column("description", String(50)),
            Column("quantity", Integer, nullable=False),
            Column("seller_id", Integer, nullable=False),

            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable = True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Product,self.products_table)

    def get_products(self, seller_id):
        
        with self.session_factory() as session:
            
            seller = session.query(Seller).filter(Seller.id == seller_id, Seller.store_address != None, Seller.deleted_at == None).all()
            
            products = session.query(Product).filter_by(seller_id= seller_id, deleted_at = None).all()
            
            return [products,seller]
    
    def get_all_products(self):
        
        with self.session_factory() as session:
            #tomo el id del vendedor de cada uno de los productos que hay actualmente
            products_seller_id = session.query(Product.seller_id).filter(Product.quantity>0, Product.deleted_at == None).all()
            sellers=[]

            #creo un query con todos los productos que hay en existencia y stock
            products= session.query(Product).filter(Product.quantity>0, Product.deleted_at == None).all()

            #evaluo con el id de los vendedores si todos tienen la dirección de tienda ya actualizada
            for id in products_seller_id:
                
                query=session.query(Seller.id).filter(Seller.id == id[0], Seller.store_address != None, Seller.deleted_at == None).all()
                if not query:
                    #si no tiene dirección lo agrego en una lista para despues borrarlos de la lista del query de products
                    sellers.append(id[0])
            
            for id_seller in set(sellers):
                #Borro duplicados con set y busco en productos cada uno de los productos del vendedor que no tienen dirección y si encuentra, lo borra de la lista
                query= session.query(Product).filter(Product.seller_id==id_seller, Product.quantity>0, Product.deleted_at == None).all()
                if query:
                    for product in query: 
                        products.remove(product)               

            
            return products

    def get_product(self, seller_id, product_sku):
        
        with self.session_factory() as session:
            
            product = session.query(Product).filter_by(sku = product_sku, seller_id= seller_id, deleted_at = None).first()

            return product

    def create_product(self, product, seller_id):
        print(seller_id)
        with self.session_factory() as session:
            query=session.query(Seller.id).filter(Seller.id == int(seller_id), Seller.store_address != None, Seller.deleted_at == None).all()
            if not query:
                return None
            session.add(product)
            session.commit()
        return product

    def update_product(self, seller_id, product_sku, fields):

        # Actualiza sólo los campos de la lista "fields" en el usuario especificado.
        # Luego retorna el producto con los nuevos datos.
        
        with self.session_factory() as session:

            session.query(Product).filter_by(sku = product_sku, seller_id= seller_id, deleted_at = None).update(fields)
            session.commit()
            
            product = session.query(Product).filter_by(sku = product_sku, deleted_at = None).first()
            return product

    def hard_delete_product(self, seller_id, product_sku):

        with self.session_factory() as session:

            product = session.query(Product).get({"sku": product_sku, "seller_id": seller_id})
            session.delete(product)
            session.commit()

    def hard_delete_all_products(self):

        if self.test:

            with self.session_factory() as session:
                
                session.query(Product).delete()
                session.commit()

    def drop_products_table(self):

        if self.test:
            self.client.drop_table(self.products_table)