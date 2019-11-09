"""
config.py
^^^^^^^^^
This file contains a global store of the configurations which are
consumed from the service's environment.
"""

import os

default_data_directory = '/data'
default_server_port = 8080
default_server_address = '0.0.0.0'
default_production = False
default_db_host = '127.0.0.1'
default_db_port = 3306
default_db_user = 'username'
default_db_password = 'password'
default_db_database = 'database'
default_db_table = 'table'
default_db_table_tmp = 'tmp'

# application configuration
production = os.environ.get('PRODUCTION', default_production)
address = os.environ.get('SERVER_ADDRESS', default_server_address)
port = os.environ.get('SERVER_PORT', default_server_port)
data_directory = os.environ.get('DATA_DIR', default_data_directory)

# database to read data from
read_db_host = os.environ.get('PROD_HOST', default_db_host)
read_db_port = os.environ.get('PROD_PORT', default_db_port)
read_db_user = os.environ.get('PROD_USER', default_db_user)
read_db_password = os.environ.get('PROD_PASSWORD', default_db_password)
read_db_database = os.environ.get('PROD_DBNAME', default_db_database)
read_db_table = os.environ.get('PROD_TABLENAME', default_db_table)

# database to write data to
write_db_host = os.environ.get('PROD_SEP_HOST', default_db_host)
write_db_port = os.environ.get('PROD_SEP_PORT', default_db_port)
write_db_user = os.environ.get('PROD_SEP_USER', default_db_user)
write_db_password = os.environ.get('PROD_SEP_PASSWORD', default_db_password)
write_db_database = os.environ.get('PROD_SEP_DBNAME', default_db_database)
write_db_table = os.environ.get('PROD_SEP_TABLENAME', default_db_table)
write_db_table_tmp = os.environ.get('PROD_SEP_TABLENAME_2', default_db_table_tmp)

# database to store the extracted piis in
pii_db_host = os.environ.get('PII_DB_HOST', default_db_host)
pii_db_port = os.environ.get('PII_DB_PORT', default_db_port)
pii_db_user = os.environ.get('PII_DB_USER', default_db_user)
pii_db_password = os.environ.get('PII_DB_PASSWORD', default_db_password)
pii_db_database = os.environ.get('PII_DB_DBNAME', default_db_database)
pii_db_table = os.environ.get('PII_DB_TABLENAME', 'pii')
