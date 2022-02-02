# Constantes que definen el "esquema" del payload que hay que validar
# para el caso de crear o actualizar un libro. Estos esquemas son usados
# en el decorador "validate_schema_flask" usado en los blueprints.

# La diferencia entre el esquema de creación y el de actualización es que
# en este último los campos son opcionales, y en algunos casos algunos campos
# podrían sólo definirse en la creación pero no permitir su actualización.

PRODUCT_CREATION_VALIDATABLE_FIELDS = {

    "sku": {
        "required": True,
        "type": "string",
    },
    "product_name": {
        "required": True,
        "type": "string",
    },
    "description": {
        "required": True,
        "type": "string",
    },

    "quantity": {
        "required": True,
        "type": "integer",
    },

}

PRODUCT_UPDATE_VALIDATABLE_FIELDS = {
   
    "username": {
        "required": False,
        "type": "string",
    },

    "password": {
        "required": False,
        "type": "string",
    },
    "shipping_address": {
        "required": False,
        "type": "string",
    },

}
