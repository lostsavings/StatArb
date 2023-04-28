import os
import yaml
from sqlalchemy import create_engine, URL


def get_psql_config():
    config_path = os.path.join('configs', 'psql.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


PSQL_CONFIG = get_psql_config()


def get_db_con():
    url = URL.create(
        "postgresql+psycopg2",
        **PSQL_CONFIG
    )
    return create_engine(url).connect()