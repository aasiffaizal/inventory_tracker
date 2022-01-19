# Inventory Tracker ![Actions](https://github.com/aasiffaizal/inventory_tracker/workflows/Run%20Tests/badge.svg?event=push&branch=main) [![codecov](https://codecov.io/gh/aasiffaizal/inventory_tracker/branch/main/graph/badge.svg?token=XD4827H15C)](https://codecov.io/gh/aasiffaizal/inventory_tracker)
An inventory tracking web application than can be used for logistics company. Currently basic CRUD operations and 
download CSV of items are implemented. The application is currently deployed in heroku in the below link.

[https://shopify-inventory-tracker-task.herokuapp.com/](https://shopify-inventory-tracker-task.herokuapp.com/)

The application is documented using swagger and can be found in handle `http://{{base_url}}/docs`. The docs for the 
hosted application can be found [here](https://shopify-inventory-tracker-task.herokuapp.com/docs).

The steps for running the application locally are also provided below.


## Table of Contents

* **[Installation](#installation)**
  * [MySQL](#mysql)
  * [Python](#python)
* **[Dependencies](#dependencies)**
* **[Running the Application](#running-the-application)**
* **[Test Coverage](#test-coverage)**
* **[API Collection](#api-collection)**

## Installation
### MySQL
MySQL is used as the database for this application hence it is required to have it in the system. The steps that needs 
to be followed to install MySQL 8.0 for any OS is found [here](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/).
Once it is set up import the schema from `schema.sql` using following commands:

```shell
mysql -hhost -uusername -Ddatabase_name -ppassword < schema.sql
```

Make sure the database with the name is created first before executing the above command.
### Python
The application is developed with python 3.10.1, hence its compatibility with previous versions is not tested. Using a 
virtual environment is recommended if the python version installed in the system does not match the version specified.
The installation of [pyenv](https://github.com/pyenv/pyenv) in is explained below.
1. Install the python build dependencies for your operating system. It can be found [here](https://github.com/pyenv/pyenv/wiki#suggested-build-environment).
2. Install pyenv using the steps provided in this [link](https://github.com/pyenv/pyenv#installation) depending on your OS.
3. Install python 3.10.1.
    ```shell
    pyenv install 3.10.1
    ```
4. Create a virtual environment for the app.
    ```shell
    pyenv virtualenv 3.10.1 inventory_tracker
    ```
5. In the application folder run the following command to localize the environment of the folder:
    ```shell
    pyenv local inventory_tracker
    ```

## Dependencies
The dependencies can be installed by using the following command.
```shell
pip install -r requirements.txt
```

## Running the Application
The DB configuration should be set as environment variables in order to run the application. The following commands can
be used to set the DB config.

```shell
export ENGINE="mysql" 
export HOST="hostname"
export USER="username"
export DB="database name"
export PASSWORD="password"
```
To run the application, use the following command.
```shell
uvicorn main:app
```

By default, the app runs in 8000 port. It can be changed by providing the argument `--port $PORT` where `$PORT` is 
replaced with the desired port number.

## Test Coverage
The code coverage is approximately 99% as tests aren't written for database model class. The tests can be run by using 
the following command:
```shell
coverage run -m pytest --verbose --failed-first --disable-pytest-warnings
```
Whereas the report of the coverage can be generated using the below command:
```shell
coverage report
```
## API Collection
The [postman](https://www.postman.com/) collection for the APIs are can be found [here](https://www.getpostman.com/collections/f005668a50bc30d91462).
These API urls are given an environmental variable `base_url` so that any url can be assigned to the variable, be it 
local or production. With either the postman webapp or desktop app, import with link function can be used import the collection.
The data is of the body is filled for the APIs but make sure to change the unique values to avoid data integrity error.