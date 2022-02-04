
from flask import Blueprint, request
from sqlalchemy import exc
import hashlib

from enviame.inputvalidation import validate_schema_flask, SUCCESS_CODE, FAIL_CODE

from src.users.http.validation import users_validatable_fields

# Endpoints para CRUD de usuarios.

# Sólo se encarga de recibir las llamadas HTTP y le entrega los datos
# relevantes a los casos de uso correspondientes. Esta capa no debe
# contener lógica de negocio, sólo lo necesario para recibir y entregar
# respuestas válidas al mundo exterior.

# Se realiza la validación de datos de entrada mediante el decorador 
# "@validate_schema_flask", el cual recibe como argumento un diccionario definido
# en el archivo "book_validatable_fields". No sólo valida que todos los campos
# requeridos vengan en el payload, sino que también que no vengan campos de más.

def create_users_blueprint(manage_users_usecase):

    blueprint = Blueprint("users", __name__)

    @blueprint.route("/users", methods = ["GET"])
    def get_users():

        users = manage_users_usecase.get_users()

        users_dict = []
        for user in users:
            users_dict.append(user.serialize())

        data = users_dict
        code = SUCCESS_CODE
        message = "Users obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }
        
        return response, http_code

    @blueprint.route("/users/<string:user_id>", methods = ["GET"])
    def get_user(user_id):

        user = manage_users_usecase.get_user(user_id)

        if user:
            data = user.serialize()
            code = SUCCESS_CODE
            message = "User obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"User of ID {user_id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data
        
        return response, http_code

    @blueprint.route("/users", methods = ["POST"])
    @validate_schema_flask(users_validatable_fields.USER_CREATION_VALIDATABLE_FIELDS)
    def create_user():

        body = request.get_json()
        body['password']= hashlib.md5(str(body['password']).encode('utf-8')).hexdigest()

        try:
            user = manage_users_usecase.create_user(body)
            data = user.serialize()
            
            code = SUCCESS_CODE
            message = "User created succesfully"
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

    @blueprint.route("/users/<string:user_id>", methods = ["PUT"])
    @validate_schema_flask(users_validatable_fields.USER_UPDATE_VALIDATABLE_FIELDS)
    def update_user(user_id):

        body = request.get_json()
        if body['password']:
            body['password']= hashlib.md5(str(body['password']).encode('utf-8')).hexdigest()

        try:
            user = manage_users_usecase.update_user(user_id, body)
            data = user.serialize()
            message = "User updated succesfully"
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

    @blueprint.route("/users/<string:user_id>", methods = ["DELETE"])
    def delete_user(user_id):

        try:
            manage_users_usecase.delete_user(user_id)
            code = SUCCESS_CODE
            message = f"User of ID {user_id} deleted succesfully."
            http_code = 200

        except ValueError as e:
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        return response, http_code

    return blueprint
