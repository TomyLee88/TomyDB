import os
# if is work this is config for now 
# TO-DO research additional way of configuration and deep understanding of all parts of configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'not-set')

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')