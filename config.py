class Config:
    # MySQL database configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Change this if you have set a password for MySQL
    MYSQL_DB = 'healthconnect'
    MYSQL_PORT = 3306  # Default MySQL port

    # Secret key for session management (for Flask apps)
    SECRET_KEY = 'your_secret_key_here'

    # Optionally enable debug mode
    DEBUG = True
