#!/usr/bin/env python3
# coding=utf-8

__author__ = 'finalsatan'

'''
Models for user, blog, comment.
'''

import time
import uuid
from orm import *

def next_id():
    return '%015d%s000' % ( int( time.time() * 1000 ), uuid.uuid4().hex )

class User( Model ):
    __table__ = 'users'
    
    id = StringField( primary_key = True, default = next_id, ddl = 'varchar(50)' )
    email = StringField( ddl = 'varchar(50)' )
    passwd = StringField( ddl = 'varchar(50)' )
    admin = BooleanField()
    name = StringField( ddl = 'varchar(50)' )
    image = StringField( ddl = 'varchar(500)' )
    created_at = FloatField( default = time.time )

class Blog( Model ):
    __table__ = 'blogs'
    id = StringField( primary_key = True, default = next_id, ddl = 'varchar(50)' )
    user_id = StringField( ddl = 'varchar(50)' )
    user_name = StringField( ddl = 'varchar(50)' )
    user_image = StringField( ddl = 'varchar(500)' )
    name = StringField( ddl = 'varchar(50)' )
    summary = StringField( ddl = 'varchar(200)' )
    content = TextField()
    created_at = FloatField( default = time.time )

class Comment( Model ):
    __table__ = 'comments'

    id = StringField( primary_key = True, default = next_id, ddl = 'varchar(50)' )
    blog_id = StringField( ddl = 'varchar(50)' )
    user_id = StringField( ddl = 'varchar(50)' )
    user_name = StringField( ddl = 'varchar(50)' )
    user_image = StringField( ddl = 'varchar(500)' )
    content = TextField()
    created_at = FloatField( default = time.time )


class Post( Model ):
    __table__ = 'posts'
    id = StringField( primary_key = True, default = next_id, ddl = 'varchar(50)' )
    post_type = StringField( ddl = 'varchar(50)' )
    post_title = StringField( ddl = 'varchar(500)' )
    post_owner = StringField( ddl = 'varchar(100)' )
    post_content = TextField()
    post_link = StringField( ddl = 'varchar(500)' )
    post_time = FloatField( default = time.time )
    created_at = FloatField( default = time.time )

class App( Model ):
    __table__ = 'apps'
    id = StringField( primary_key = True, default = next_id, ddl = 'varchar(50)' )
    app_name = StringField( ddl = 'varchar(500)' )
    app_link = StringField( ddl = 'varchar(500)' )
    app_time = FloatField( default = time.time )
    created_at = FloatField( default = time.time )