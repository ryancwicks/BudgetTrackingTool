import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('BUDGET_TRACKER_SECRET_KEY') or 'Temporary hard to guess key.',
    CERTIFICATE_LOCATION = os.environ['BUDGET_TRACKER_CERTIFICATE']

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
