from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import json
import os

def get_base():
    return Base

def get_engine():
    return engine


json_file = json.load(open('config.json'))
database = json_file['database']

if json_file['path'] == 'ROOT_DIR':
    path = os.path.dirname(os.path.abspath('__init__.py'))
else:
    path = json_file['path']

engine = create_engine('sqlite:///'+os.path.abspath(path+'/'+database))
Base = declarative_base()
database_type = json_file['type']

if database_type == "sqlite":
    from sqlalchemy.dialects.sqlite import INTEGER
    unsigned_int = INTEGER()
elif database_type == "mysql":
    from sqlalchemy.dialects.mysql import INTEGER
    unsigned_int = INTEGER(unsigned=True)


