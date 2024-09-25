# Sampader
A small-scale social media app
## Table of Contents
- [Description](#description)
- [Getting Started](#getting-started)
  - [Dependencies](#dependencies)
  - [Configs File](#configs-file)
  - [Executing the Code](#executing-the-code)
- [Code Overview](#code-overview)
  - [Database](#database)
  - [API](#api)
  - [Admin](#admin)
- [License](#license)


## Description
A social media app, similar to Twitter but built to be used in smaller scales. Users can post a text or an image, leave a comment on other users' posts, like a post and follow or block others. This repository includes back-end codes and structure of the project. The APIs are action-based and there are examples of requesting APIs available in `/Sampader/test/api` folder.
## Getting Started
First you need to clone the repository on your machine.
### Dependencies
Before starting the app you need to install the packages and modules mentioned `requirements.txt` as follows:
```
pip install -r requirements.txt
```
### configs file
You need a `configs.py` file in your project's root directory to store secret keys and paths:
```python
SECRET_KEY = "smpd418"
UPLOADS_PATH = "F://Sampader/uploads"
URL_PATH = "http://127.0.0.1:5000"
ADMIN_ROOT_PATH = "F://Sampader/admin"
DB_PATH = "F://Sampader/database/data.db"
SESSION_KEY = "some key to encode sessions"
DATABASE_URI = "sqlite:///database/data.db"
```
### Executing the code
Run the `run.py` file or use this command:
```
python run.py
```
## Code overview
This project uses the Flask micro-framework, and the code structure follows the standard modular form. The `uploads` and `tests` folders are used in typical ways. The `templates` folder is for `admin` module templates, and the `statics` folder contains static files for styling these templates.
### database
To interact with database `SQLAlchemy` is used as ORM. Here a SQLite data base is used (located in `/Sampader/database/data.db`). There are three models for users, posts (and comments) and notifications. There are also three association tables to handle many-to-many relationships.
### api
There are four blueprints, each in a different file, to handle various API routes (there are 25 APIs in total). They are all combined to create an app object in the `__init__.py` file.
Each API does not interact with the database directly but uses the `services` module to handle the main logic and functionality. Each blueprint is related to a corresponding service file in that module.
Almost all routes are protected and require authentication headers. A JSON Web Token (JWT) is used to authenticate users. To prevent DOS attacks, the `flask-limiter` module is used as an extension.
### admin
The `admin` module is a semi-independent Flask app that provides the admin direct access to query the database. It is connected to the rest of the project in the `run.py` file.
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
