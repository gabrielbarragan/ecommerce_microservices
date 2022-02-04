# Project Name: ecommerce microservices 

### Description

This project use the following template [siguiente repositorio](https://github.com/enviame/backend-test-2.0/tree/main/docker-python) and the [clean architecture](https://www.oreilly.com/library/view/clean-architecture-a/9780134494272/) principles.

This project use [Flask](https://flask.palletsprojects.com/) and [SQL Alchemy](https://www.sqlalchemy.org/).

### Construction 🛠️
* **Language:** Python 3
* **Framework:** Flask, SQL Alchemy

## Requirements
- Docker installed

## Installation and execution

- Clone  this project.
- Copy **.env.example** to **.env**. It will be used as environment variables source.
- Inside Docker/app folders of ecommerce-service:
* Copy **.env.example** to **.env**. It will be used as environment variables source.

Run ```docker-compose``` command inside **project** folder.

* Building the containers: ```docker-compose build```

* Starting the services: ```docker-compose up -d```

* Stoping the services: ```docker-compose stop```

By default the ecommerce-microservices will run under the following ports 8000


Check the **.env.example** file to change these or any other params.

#### Note
The Flask application will probably throw an exception the first time, because it will try to connect to the MySQL service that is still initializing for the first time; in this case wait for MySQL to fully initialize first and then run the command `docker-compose restart $NAME_SERVICE` in another terminal to restart the crashed service.


### Testing ⚙️


To run manual tests, the examples are in `req.http` file is included with requests to localhost. 

To tests into **Postman**, import file **["ecommerce_microservices_test.postman_collection.json"](https://github.com/gabrielbarragan/ecommerce_microservices/blob/main/ecommerce_microservices_test.postman_collection.json)** in postman app. There you will find test data and available endpoints.

To run the tests:

- Have the services running using `docker-compose up`.
- In another console, run `docker exec ecommerce-service python -m pytest -rP` (only tests are available for users).

The `-rP` flag is optional, and is used to display in the console the `print()` done during the tests, otherwise `pytest` will hide them, only showing them in case the test has failed.

Repository tests write data to container databases, but write them to temporary tables or collections with the suffix "\ _test" that are deleted once they are finished, so as not to carry the actual data. Bear in mind that in the case of Firestore there is no data persistence yet; if the service is lowered and raised again, the previous data is lost.

## endpoints and examples for manual tests:

### Crear un usuario:
POST http://localhost:8000/users
```
{
            "username": "Leodavinci",
            "email": "Davinci@renacimiento.com",
            "first_name": "Leonardo",
            "last_name": "Davinci",
            "password": "Leo.2022",
            "shipping_address": "Florencia"
}
```
### Obtener todos los usuarios:
GET http://localhost:8000/users

### Obtener un usuario por id:
GET http://localhost:8000/users/1

### Actualizar un usuario:
PUT http://localhost:8000/users/1
```
{
            "password": "Leo.200000",
            "shipping_address":"Florencia calle 2"

}
```
### Borrar un usuario
DEL http://localhost:8000/users/1


### Crear un vendedor:
POST http://localhost:8000/admin/sellers
```
{
            "username": "Niko",
            "email": "Niko@niko.com",
            "first_name": "Nikoleto",
            "last_name": "Marci",
            "password": "Niko.202222",
            "description": "El mejor vendedor"
}
```
### Obtener todos los vendedores:
GET http://localhost:8000/admin/sellers


### Obtener un vendedor por id:
GET http://localhost:8000/sellers/1

### Actualizar un vendedor:
PUT http://localhost:8000/sellers/1
```
{
        "store_address": "mega l43"

}
```
### Borrar un vendedor:
DEL http://localhost:8000/admin/sellers/1



### Crear un producto:
POST http://localhost:8000/seller/1/products
```
{
            "sku": "sku0001",
            "product_name": "Golosinas",
            "description": "Golosinas deliciosas",
            "quantity": 20
}
```
### Obtener todos los productos de un vendedor (requiere que la store_address no esté vacía):
GET http://localhost:8000/seller/1/products

### Obtener todos los productos:
GET http://localhost:8000/products

### Obtener un producto por sku:
GET http://localhost:8000/seller/1/products/sku0001

### Actualizar un product:
PUT http://localhost:8000/seller/1/products/sku0002
```
{
            "product_name":"Caramelos",
            "description": "Deliciosos caramelos",
            "quantity":7

}
```

### Borrar un producto
DEL http://localhost:8000/seller/1/products/sku0002


### Autores ✒️
* **Autor del ecommerce microservice:** Gabriel Rondón Barragán.

* **Autor de la plantilla original:** Hans Auzian C., hans.auzian@enviame.io.