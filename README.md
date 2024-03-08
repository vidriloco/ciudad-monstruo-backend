# Ciudad Monstruo

### How to deploy

1. Clone this github repo
2. Install Docker
3. Prepare the docker image doing `docker compose build` or `docker-compose build`
4. Make sure the mapping of ports is correct in the `docker-compose.yaml` file
5. Run the docker image by doing: `docker compose up` or `docker-compose up`

If all goes alright, the docker instance should be running. Now, connect to the app server and prepare the database and seed data:

1. By doing `docker ps` you can find the running docker instances
2. Connect to the instance by doing: `docker exec -it <container name> /bin/bash`
3. Run the migrations: `python3 manage.py migrate` from the geodjango directory
4. Import the data from the CSV file: `python3 manage.py loadvictims`
5. Create superuser by doing `python manage.py createsuperuser`

### How to connect with DB

Use this: `psql -U geodjango -d gis`

### How to migrate down

python3 manage.py migrate world 0010 will undo the migration starting with 0010

### Show the available migrations

python3 manage.py showmigrations world