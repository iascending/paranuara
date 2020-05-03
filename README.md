# paranuara
Paranuara Challenge
docker build .
docker-compose build
docker-compose up
docker-compose run --rm app sh -c "python manage.py test && flake8"
<!-- docker-compose run --rm app sh -c "python manage.py startapp user" -->