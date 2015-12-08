#!/usr/bin/env python3
# coding=utf-8

'''
import asyncio
import orm
from models import User,Blog,Comment

def test_user( loop ):
    yield from orm.create_pool( loop = loop, user = 'ubuntu', password = 'ubuntu', db = 'personalblog' )
    u = User( name = 'Test', email = 'test@example.com', passwd = '12345678', image = 'about:blank' )
    yield from u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete( test_user(loop) )
loop.close()
'''

import sys
import orm,asyncio
from models import User,Blog,Comment


def test( loop ):
    yield from orm.create_pool( loop = loop, user='ubuntu', password='ubuntu', db='personalblog' )
    u=User(name='test3',email='test3@test.com',passwd='test',image='about:blank')
    yield from u.save()

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete( asyncio.wait([test( loop )]) )  
    loop.close()
    if loop.is_closed():
        sys.exit(0)