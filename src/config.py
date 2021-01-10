db = {
    'user' : 'root',
    'password' : 'rlagkwjd0318',
    'host' : '127.0.0.1',
    'port' : '3306',
    'database' : 'magicbox_flask'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"