## Initial Setup:
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

The default sqlite database will likely serve your needs just fine.
If that's the case, just run:

    flask db upgrade

Otherwise, to connect to an existing PostgreSQL or MySQL server, create an empty database called "totlahtol" and create a .env file in this directory with the following line:

#### Postgres

    DATABASE_URL="postgresql+psycopg3://yourdatabaseusername:yourdatabasepassword@localhost:5432/totlahtol"


#### MySQL

    DATABASE_URL="mysql+pymysql://yourdatabaseusername:yourdatabasepassword@localhost:3306/totlahtol"
Since pymysql isn't included in requirements.txt, we'll have to install it:

    pip install pymysql

#### Finally:


    flask db upgrade