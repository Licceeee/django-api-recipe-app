docker-compose run app sh -c "python manage.py makemigrations"
docker-compose run app sh -c "python manage.py migrate"
