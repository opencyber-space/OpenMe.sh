import os

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_USER = os.getenv('DB_USER', 'user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_NAME = os.getenv('DB_NAME', 'message_db')
    
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_QUEUE = 'MESSAGES'
    
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))
    BATCH_INTERVAL = int(os.getenv('BATCH_INTERVAL', 10))  # in seconds
