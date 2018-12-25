'''Set environment specific configurations here'''
import os


class Config:
    '''parent configuration class, contains all general configuration settings'''
    FLASK_DEBUG = False
    SECRET_KEY = os.getenv('SECRET')
    ENV = os.environ.get('APP_SETTINGS')

class DevelopmentConfig(Config):
    '''Configurations for development. contains configuration settings specific to development'''
    FLASK_DEBUG = True
    DATABASE_URL = os.getenv('DEVELOPMENT_DATABASE')
    
    

class TestingConfig(Config):
    '''Configuration settings specific to testing environment'''
    FLASK_DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('TESTING_DATABASE')


class ProductionConfig(Config):
    '''Configuration settings specific to production environment'''
    FLASK_DEBUG = False
    TESTING = False
    DATABASE_URL = os.getenv('PRODUCTION_DATABASE')

config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production':ProductionConfig
}