
# Paranuara Challenge

## Installation


To build and run the project, Docker and docker-compose are required on the machine.

Download and install Docker: https://www.docker.com/products/docker-desktop


## Build


Go to the directory you would like the project to be. Then take the following steps in terminal:

1. git clone git@github.com:iascending/paranuara.git

2. cd paranuara

3. docker build .

4. docker-compose build


## Unit tests


Run the following commands in the root directory of the project:

1. docker-compose run app sh -c "python manage.py migrate"

2. docker-compose run --rm app sh -c "python manage.py test && flake8"


## API Endpoints:


Before making API calls to the API endpoints of the project, please start development server first.

To start server in terminal, in the root directory of the project, run:

`docker-compose up'

### Create registered user
- url: http://127.0.0.1:8000/api/user/create/
- permission: any
- method: `POST`
- headers: `None`
- body fields: {'email': 'youremail@gmail.com', 'password': 'yourpass', 'name': 'Any Name'}
- response:
    {
        "email": "myemail@gmail.com",
        "name": "Test User"
    }

### Get user authentication token
- url: http://127.0.0.1:8000/api/user/token/
- permission: authenticated user
- method: `POST`
- headers: `None`
- body fields: {"email": "youremail@gmail.com", "password": "yourpass"}
- response:
    {
        "token": "948de8cc655a404783f7b162c1e22066e12334d0"
    }

### List all employees belong to specific company
- url: http://127.0.0.1:8000/api/employees/?company={company_index}
- permission: authenticated user
- method: `GET`
- headers: {'AUTHORIZATION': 'Token 948de8cc655a404783f7b162c1e22066e12334d0'}
- body fields: `None`
- response:
    [
        {
            "employees": [
                {
                    "index": 363,
                    "name": "Herrera Powers"
                },
                {
                    "index": 790,
                    "name": "Emerson Kennedy"
                },
            ]
        }
    ]

 ### Given 2 people, provide their Name, Age, Address, phone and the list of their friends in common which have brown eyes and are still alive.
- url: http://127.0.0.1:8000/api/friends/?index1={people1_index}&index2={people2_index}
- permission: authenticated user
- method: `GET`
- headers: {'AUTHORIZATION': 'Token 948de8cc655a404783f7b162c1e22066e12334d0'}
- body fields: `None`
- response:
    {
        "people1": {
            "name": "Collins Berger",
            "age": 52,
            "address": "931 Amboy Street, Fredericktown, Washington, 9655",
            "phone": "+1 (861) 413-3809"
        },
        "people2": {
            "name": "Wendy Leon",
            "age": 25,
            "address": "957 Vista Place, Guilford, Texas, 4016",
            "phone": "+1 (831) 408-2309"
        },
        "common_friends": [
            {
                "name": "Decker Mckenzie",
                "age": 60,
                "address": "492 Stockton Street, Lawrence, Guam, 4854",
                "phone": "+1 (893) 587-3311"
            },
            {
                "name": "Mindy Beasley",
                "age": 62,
                "address": "628 Brevoort Place, Bellamy, Kansas, 2696",
                "phone": "+1 (862) 503-2197"
            }
        ]
    }

### Given 1 people, provide a list of fruits and vegetables they like.
- url: http://127.0.0.1:8000/api/fruits/?index={people_index}
- permission: authenticated user
- method: `GET`
- headers: {'AUTHORIZATION': 'Token 948de8cc655a404783f7b162c1e22066e12334d0'}
- body fields: `None`
- response:
    [
        {
            "username": "Bradshaw Nichols",
            "age": 50,
            "fruits": [
                "banana"
            ],
            "vegetables": [
                "cucumber",
                "beetroot",
                "celery"
            ]
        }
    ]
