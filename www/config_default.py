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
        'user' : '******',
        'password' : '******',
        'dbname' : '******'
    },
    'server' : {
        'server_ip' : '127.0.0.1',
        'server_port' : 9000
    },
    'forum' : {
        'username' : '******',
        'password' : '******'
    },
    'email' : {
        'sender' : '******@gmail.com',
        'subject' : 'HiPda Buy & Sell News',
        'smtpserver' : 'smtp.gmail.com',
        'smtpport' : 587,
        'username' : '******@gmail.com',
        'password' : '******'
    },
    'time_interval' : {
        0 : 480,
        8 : 60,
        9 : 60,
        10 : 60,
        11 : 60,
        20 : 15,
        21 : 15,
        -1 : 30
    },
    'session' : {
        'secret' : '******',
        'COOKIE_NAME' : '******'
    }
}
