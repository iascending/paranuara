# paranuara
Paranuara Challenge
1. install docker and docker-compose
2. git clone paranuara
3. cd paranuara
4. docker build .
5. docker-compose build
6. docker-compose run app sh -c "python manage.py makemigrations core"
<!-- docker-compose run app sh -c "python manage.py makemigrations --empty core" -->
7. docker-compose up
docker-compose run --rm app sh -c "python manage.py test && flake8"
<!-- docker-compose run --rm app sh -c "python manage.py startapp user" -->