# src/config.py
import configparser

def load_config_db(config_file='conf/config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['database']

def get_connection_string(params):
    return f"postgresql+psycopg2://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}"