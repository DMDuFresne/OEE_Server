class Config(object):
    DEBUG = False
    TESTING = False
    # any other configuration options can go here


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
