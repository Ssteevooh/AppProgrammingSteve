class Config:
    DEBUG = True

    SECRET_KEY = 'super-secret-key'

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://matonet:supermato@localhost:5432/matonet_db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ERROR_MESSAGE_KEY = 'message'

    # JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
