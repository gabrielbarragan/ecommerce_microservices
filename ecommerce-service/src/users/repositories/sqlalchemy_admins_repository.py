from sqlalchemy import Table, Column, Integer, String, ForeignKey, TIMESTAMP


from src.users.entities.admin import Admin
    
# Implementación con SQL Alchemy para el repositorio de usuarios.


class SQLAlchemyAdminsRepository():

    def __init__(self, sqlalchemy_client, test = False):

        # Mapear la tabla Book de forma imperativa.
        # Si "test" es true, se le agrega un sufijo al nombre de la tabla,
        # para que las pruebas de integración no sobreescriban los datos existentes.

        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.test = test

        table_name = "Admins"

        if test:
            table_name += "_test"

        self.admins_table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key = True),
            Column("username", String(50), unique=True),
            Column("first_name", String(50)),
            Column("last_name", String(50)),
            Column("email", String(50), unique=True, nullable=False),
            Column("password", String(50)),

            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable = True),
        )

        sqlalchemy_client.mapper_registry.map_imperatively(Admin, self.admins_table)

    def get_admins(self):
        
        with self.session_factory() as session:
            
            admins = session.query(Admin).filter_by(deleted_at = None).all()
            return admins

    def get_admin(self, id):
        
        with self.session_factory() as session:

            admin = session.query(Admin).filter_by(id = id, deleted_at = None).first()
            return admin

    def create_admin(self, admin, email):

        with self.session_factory() as session:
            session.add(admin)
            session.commit()
        return admin

    def update_admin(self, id, fields):

        # Actualiza sólo los campos de la lista "fields" en el usuario especificado.
        # Luego retorna el usuario con los nuevos datos.
        
        with self.session_factory() as session:

            session.query(Admin).filter_by(id = id, deleted_at = None).update(fields)
            session.commit()
            
            admin = session.query(Admin).filter_by(id = id, deleted_at = None).first()
            return admin

    def hard_delete_admin(self, id):

        with self.session_factory() as session:

            admin = session.query(Admin).get(id)
            session.delete(admin)
            session.commit()

    def hard_delete_all_admins(self):

        if self.test:

            with self.session_factory() as session:
                
                session.query(Admin).delete()
                session.commit()

    def drop_admins_table(self):

        if self.test:
            self.client.drop_table(self.admins_table)