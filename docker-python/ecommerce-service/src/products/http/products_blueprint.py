from flask import Blueprint, request
from sqlalchemy import exc

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE

from src.products.http.validation import products_validatable_fields


# Endpoints para CRUD de usuarios.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador 
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "book_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.

def create_products_blueprint(manage_products_usecase):

    blueprint = Blueprint("products", __name__)

    @blueprint.route("/products", methods = ["GET"])
    def get_all_products():
        """Endpoint for show all products to the users 
           No parameters"""

        products = manage_products_usecase.get_all_products()
        
        products_dict = []


        if products:

            for product in products:
                products_dict.append(product.serialize())

            data = products_dict
            code = SUCCESS_CODE
            message = "Products obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = "No products finded"
            http_code = 400

        response = {
            "code": code,
            "message": message,
            "data": data,
        }
        
        return response, http_code

    @blueprint.route("/seller/<string:seller_id>/products", methods = ["GET"])
    def get_products(seller_id):
        """Endpoint for show all products of an specific seller"""

        products, seller = manage_products_usecase.get_products(seller_id)
        
        products_dict = []

        if not seller:
            data = None
            code = FAIL_CODE
            message = "No products to show for this seller or this seller doesn't exists"
            http_code = 400

        elif products:

            for product in products:
                products_dict.append(product.serialize())

            data = products_dict
            code = SUCCESS_CODE
            message = "Products obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = "No products finded"
            http_code = 400

        response = {
            "code": code,
            "message": message,
            "data": data,
        }
        
        return response, http_code
    @blueprint.route("/seller/<string:seller_id>/products/<string:product_sku>", methods = ["GET"])
    def get_product(seller_id, product_sku):
        """Endpoint for show all products of an specific seller and product id"""

        product= manage_products_usecase.get_product(seller_id, product_sku)
        

        if product:
            data = product.serialize()
            code = SUCCESS_CODE
            message = "Product obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = "Product  doesn't exists"
            http_code = 400    

        response = {
            "code": code,
            "message": message,
            "data": data,
        }
        
        return response, http_code
        
    
    @blueprint.route("/seller/<string:seller_id>/products", methods = ["POST"])
    @validate_schema_flask(products_validatable_fields.PRODUCT_CREATION_VALIDATABLE_FIELDS)
    def create_product(seller_id):

        body = request.get_json()
        print(body)
        try:
            user = manage_products_usecase.create_product(body, seller_id)
            data = user.serialize()
            
            code = SUCCESS_CODE
            message = "Product created succesfully"
            http_code = 201

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        except exc.IntegrityError as e:
            e_str= str(e)

            msg_start_pos = e_str.find('"')
            msg_end_pos = e_str.rfind('"')
            msg= e_str[msg_start_pos+1:msg_end_pos]

            data = None
            code = FAIL_CODE
            message = msg
            http_code = 409

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code
        

    @blueprint.route("/seller/<string:seller_id>/products/<string:product_sku>", methods = ["PUT"])
    @validate_schema_flask(products_validatable_fields.PRODUCT_UPDATE_VALIDATABLE_FIELDS)
    def update_product(seller_id, product_sku):

        body = request.get_json()

        try:
            product = manage_products_usecase.update_product(seller_id,product_sku, body)
            data = product.serialize()
            message = "Product updated succesfully"
            code = SUCCESS_CODE
            http_code = 200

        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code


    return blueprint