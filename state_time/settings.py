# -*- coding: utf-8 -*-
"""Application configuration."""
import os
import binascii


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get(
        'STATE_TIME_SECRET',
        binascii.hexlify(os.urandom(32)))  # Done.
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEBPACK_MANIFEST_PATH = 'webpack/manifest.json'


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'  # TODO: Change me
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    LOCAL_DB_NAME = 'state_time'
    LOCAL_DB_USER = 'ubuntu'
    LOCAL_DB_PASSWORD = 'ubuntu'
    LOCAL_DB_PORT = '5432'
    # Put the db file in project root
    # DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@localhost:{}/{}'.format(
        LOCAL_DB_USER,
        LOCAL_DB_PASSWORD,
        LOCAL_DB_PORT,
        LOCAL_DB_NAME)
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False  # Allows form testing
