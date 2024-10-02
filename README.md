# Sampader
A small-scale social media app

## Table of Contents
- [Description](#description)
- [Getting Started](#getting-started)
  - [Dependencies](#dependencies)
  - [Configuration File](#configuration-file)
  - [Running the Application](#running-the-application)
- [Code Overview](#code-overview)
  - [Database](#database)
  - [API](#api)
  - [Admin](#admin)
- [Testing Instructions](#testing-instructions)
- [License](#license)

## Description
Sampader is a social media app, similar to Twitter but designed for smaller-scale usage. Users can post text or images, comment on other users' posts, like posts, follow or block other users. This repository contains the back-end code for the project. API request examples are available in the `/Sampader/test/api` folder.

## Getting Started
First, you need to clone the repository to your local machine.

### Dependencies
Before starting the app, make sure you install the required packages listed in `requirements.txt` by running the following command:
```
pip install -r requirements.txt
```

### Configuration File
Create a file named `configs.py` in the project's root directory and add the following configuration settings:
```python
SECRET_KEY = "smpd418"
UPLOADS_PATH = "F://Sampader/uploads"
URL_PATH = "http://127.0.0.1:5000"
ADMIN_ROOT_PATH = "F://Sampader/admin"
DB_PATH = "F://Sampader/database/data.db"
SESSION_KEY = "some key to encode sessions"
DATABASE_URI = "sqlite:///database/data.db"
```

### Running the Application
Run the `run.py` file or use the following command in your terminal:
```
python run.py
```

## Code Overview
This project is built using the Flask micro-framework and follows a modular architecture. The `uploads` and `tests` folders serve their typical purposes. The `templates` folder is for the `admin` module's templates, and the `statics` folder contains static files for styling those templates.

### Database
SQLAlchemy is used as the Object-Relational Mapping (ORM) to interact with the database. The database is a SQLite file located at `/Sampader/database/data.db`. There are three models: Users, Posts (which includes comments), and Notifications. Additionally, three association tables handle many-to-many relationships such as follows and likes.

### API
There are four blueprints, each located in separate files, to handle various API routes (25 APIs in total). All blueprints are registered to create the Flask application instance in the `__init__.py` file. Each API route calls the `services` module to interact with the database and perform business logic. Most routes are protected and require JWT-based authentication headers. The `flask-limiter` extension is used to prevent DoS attacks.

### Admin
The `admin` module functions almost like a separate Flask application, handling its own HTML views and providing the admin with direct access to the database through a web interface. Although it operates somewhat independently, it is still integrated into the main project via a blueprint and is connected to the rest of the app in the `run.py` file.

## Testing Instructions
To test services, you can import `/Sampader/tests/services` into your test file:
```python
from tests import services
```
Then, run the test file using:
```
python test.py
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
