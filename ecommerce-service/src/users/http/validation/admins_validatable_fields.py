# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un libro. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

ADMIN_CREATION_VALIDATABLE_FIELDS = {

    "username": {
        "required": True,
        "type": "string",
    },
    "first_name": {
        "required": True,
        "type": "string",
    },
    "last_name": {
        "required": True,
        "type": "string",
    },
    "email": {
        "required": True,
        "type": "string",
    },
    "password": {
        "required": True,
        "type": "string",
    },

}

ADMIN_UPDATE_VALIDATABLE_FIELDS = {
   
    "username": {
        "required": True,
        "type": "string",
    },

    "password": {
        "required": True,
        "type": "string",
    },

}