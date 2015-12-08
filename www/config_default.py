#!/usr/bin/env python3
# coding=utf-8

'''
Default configurations.
'''

__author__ = 'finalsatan'

configs = {
    'debug' : True,
    'db' : {
        'host' : '127.0.0.1',
        'port' : 3306,
        'user' : 'ubuntu',
        'password' : 'ubuntu',
        'db' : 'personalblog'
    },
    'session' : {
        'secret' : 'Awesome'
    }
}
