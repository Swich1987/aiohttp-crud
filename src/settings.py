import os
from pathlib import Path

from dotenv import load_dotenv

cur_dir = os.path.dirname(__file__)
env_path = Path(cur_dir).parent / 'prod.env'
load_dotenv(dotenv_path=env_path, verbose=True, override=True)

POSTGRES_CRED = {
    'database': os.getenv('POSTGRES_DB'),
    'port': os.getenv('POSTGRES_PORT'),
    'username': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST')
}
