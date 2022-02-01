from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP


from src.users.entities.seller import Seller
    
# Implementación con SQL Alchemy para el repositorio de usuarios.


class SQLAlchemySellersRepository():

    def __init__(self, sqlalchemy_client, test = False):

        # Mapear la tabla Seller de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Sellers"

        if test:
            table_name += "_test"

        self.sellers_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key = True),
            Column("username", String(50), unique=True),
            Column("first_name", String(50)),
            Column("last_name", String(50)),
            Column("email", String(50), unique=True, nullable=False),
            Column("password", String(50)),
            Column("description", String(100)),
            Column("store_address", String(100)),

            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable = True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Seller, self.sellers_table)

    def get_sellers(self):
        
        with self.session_factory() as session:
            
            sellers = session.query(Seller).filter_by(deleted_at = None).all()
            return sellers

    def get_seller(self, id):
        
        with self.session_factory() as session:

            seller = session.query(Seller).filter_by(id = id, deleted_at = None).first()
            return seller

    def create_seller(self, seller, email):

        with self.session_factory() as session:
            session.add(seller)
            session.commit()
        return seller

    def update_seller(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el usuario especificado.
        # Luego retorna el usuario con los nuevos datos.
        
        with self.session_factory() as session:

            session.query(Seller).filter_by(id = id, deleted_at = None).update(fields)
            session.commit()
            
            seller = session.query(Seller).filter_by(id = id, deleted_at = None).first()
            return seller

    def hard_delete_seller(self, id):

        with self.session_factory() as session:

            seller = session.query(Seller).get(id)
            session.delete(seller)
            session.commit()

    def hard_delete_all_sellers(self):

        if self.test:

            with self.session_factory() as session:
                
                session.query(Seller).delete()
                session.commit()

    def drop_sellers_table(self):

        if self.test:
            self.client.drop_table(self.sellers_table)