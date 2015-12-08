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
        'dbname' : 'personalblog'
    },
    'server' : {
        'server_ip' : '127.0.0.1',
        'server_port' : 9000
    },
    'forum' : {
        'time_interval' : 5,
        'username' : '******',
        'password' : '******'
    },
    'email' : {
        'sender' : '******',
        'subject' : 'HiPda Buy & Sell News',
        'smtpserver' : 'smtp.gmail.com',
        'smtpport' : 587,
        'username' : '******',
        'password' : '******'
    },
    'session' : {
        'secret' : 'Awesome',
        'COOKIE_NAME' : 'awesession'
    }
}
