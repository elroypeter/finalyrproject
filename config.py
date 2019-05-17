class Config(object):
    """
    Common configurations
    """
    UPLOAD_FOLDER = '/images/crimes'
    ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlxs'])
    #put any configurations here that are common accross all environments
class ExcelConfig(Config):
    UPLOAD_FOLDER = '/images/crimes'
    ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlxs'])

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = True

app_config = {
        'development':DevelopmentConfig,
        'production':ProductionConfig,
        'image_config':ExcelConfig
    }