# cnotes
Google keep notes clone with bibtex referencing support

# Installation

Install Flask:

```
sudo apt install python3 python3-pip python3-flask python3-sqlalchemy python3-marshmallow python3-psycopg2 python3-passlib python3-flask-httpauth
pip3 install Flask-SQLAlchemy 
```

Install postgres:

```
$ sudo apt install -y postgresql postgresql-contrib postgresql-client
$ sudo systemctl start postgresql.service
```

Set up the database for the first time and change the password:

```
sudo -u postgres psql
\password
```

Create the database and connect to it:

```
postgres=# CREATE DATABASE cnotes;
postgres=# \c cnotes;
```
Create a database user:

```
postgres=# CREATE USER <username> WITH PASSWORD "password";
postgres=# GRANT ALL PRIVILEGES ON DATABASE cnotes TO <username>;
cnotes=# GRANT ALL PRIVILEGES ON TABLE users TO <username>;
cnotes=# GRANT USAGE, SELECT ON SEQUENCE users_user_id_seq TO ciaran;
```

# Run

Modify the `env.sh` file to contain your database username and password and source it:

```
$ . env.sh
```

Start the Flask API:

```
flask run --host=0.0.0.0
```