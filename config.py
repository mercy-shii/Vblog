import os
class Config:
    
    SECRET_KEY =('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mercy:shii@localhost/blogs'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    
    
class ProdConfig(Config):

       SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")



class TestConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mercy:shii@localhost/blogs_test'
    

class DevConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mercy:shii@localhost/blogs'
    DEBUG = True
    


config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}