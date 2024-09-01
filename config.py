import os

from dotenv import load_dotenv

load_dotenv()

DATABASE = {
    'dbname': os.getenv('DBNAME'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'port': 5432
}
SECRET_KEY = os.getenv('SECRET_KEY')
