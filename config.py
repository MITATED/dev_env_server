#!/usr/bin/env python
# coding: utf-8

CONFIG = {
    # API port
    'tasks_http_port': '4001',
    'profiles_http_port': '4002',
    #
    'cc_profiles_url': 'http://localhost:4002/profiles',
}


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/user/work/dev_env_cc_server/test.db'
    SECRET_KEY = 'semething very secret'

    ### Flask Security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_REGISTERABLE = True
