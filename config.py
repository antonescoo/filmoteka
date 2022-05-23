class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:191187@localhost/films'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secretnyi_secret'

    SECURITY_PASSWORD_SALT = 'jkLJKnfsmn,NJND:Mmxslkk'