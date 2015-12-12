#!/usr/bin/env python3
# coding=utf-8

__author__ = 'finalsatan'

'''
Get the Hi-Pda Buy&Sell new posts, then save in db and send emails
'''

import re
from datetime import datetime
import time
import http.cookiejar
import urllib.request, urllib.parse, urllib.error
from io import StringIO, BytesIO
import gzip
import hashlib
import mysql.connector

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

import logging
logging.basicConfig( level = logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d][%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S' )

from models import Post, next_id
from httprequest import HttpRequest
from config import configs


db_user = configs.db.user
db_passwd = configs.db.password
db_name = configs.db.dbname

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def get_post_content_and_time( post_url, post_type, post_name, time_last_time ):
    post_full_url = 'http://www.hi-pda.com/forum/' + post_url
    post_headers = {
        'Referer' : 'http://www.hi-pda.com/forum/',
        'Host'    : 'www.hi-pda.com'
    }
    
    logging.info( 'Get post[%s] by url[%s].' % ( post_name, post_url ) )

    post_request = HttpRequest( post_full_url, None, post_headers )
    try:
        post_request.send_request()
    except TimeoutError:
            logging.warn(" Request url[%s] failed. " % post_full_url)
    post_resp_content = post_request.get_resp_content()
    try:
        post_resp_content = post_resp_content.decode('gbk')
    except UnicodeDecodeError as e:
        logging.error( 'Decode post response content failed.' )
        logging.exception( e )

    #<meta name="description" content=" Hi!PDA  本帖最后由 一炮而红 于 2015-12-1 22:59 编辑 三原色智能通讯欢迎您！ http://187161236.taobao.com/ 论坛5年商家。&amp;nbsp;&amp;nbsp;微信&amp;nbsp;&amp;nbsp;QQ：18 ... - Board" />
    re_pattern_content = re.compile( r'''<meta name="description" content="(.*)" />''' )
    result_content = re_pattern_content.search( post_resp_content )

    post_content = None
    post_update_time = None
    post_create_time = None

    if result_content is None:
        logging.warn( 'Request failed.' )
    else:
        post_content = result_content.groups()[0]

    if post_content is None:
        logging.warn( 'Get post conetent failed.' )
    else:
        re_pattern_update_time = re.compile( r'''于 (.*) 编辑''' )
        result_update_time = re_pattern_update_time.search( post_content )
        if result_update_time is None:
            pass
        else:
            post_update_time = result_update_time.groups()[0]

    if post_update_time is None:
        re_pattern_create_time = re.compile( r'''<em id=".+">发表于 (.+)</em>''' )
        result_create_time = re_pattern_create_time.search( post_resp_content )
        
        if result_create_time is None:
            logging.warn( 'Get post time failed.' )
        else:
            post_create_time = result_create_time.groups()[0]
    else:
        post_create_time = post_update_time


    
    post_create_time_datetime = datetime.strptime(post_create_time, '%Y-%m-%d %H:%M')
    post_create_time_stamp = post_create_time_datetime.timestamp()

    post_create_time_stamp - time_last_time

    post = None

    if ( post_create_time_stamp - time_last_time ) > 0:

        conn = mysql.connector.connect(user = db_user, password = db_passwd, database = db_name)
        cursor = conn.cursor()
        logging.info( 'post_type:' + post_type )
        logging.info( 'post_name:' + post_name )
        logging.info( 'post_url:' + post_full_url )
        logging.info( 'post_create_time:' + post_create_time )
        logging.info( 'post_content:' + post_content )
        
        post_id = next_id()
        post = Post( id = post_id, post_type = post_type, post_title = post_name, post_owner = 'hipda', post_content = post_content, post_link = post_full_url, post_time = post_create_time )
        # post.save()
        cursor.execute('insert into posts (id, post_type, post_title, post_owner, post_content, post_link, post_time, created_at ) values (%s, %s, %s, %s, %s, %s, %s, %s)', [post_id, post_type, post_name, 'hipda', post_content, post_full_url, post_create_time_stamp, post_create_time_stamp])
        conn.commit()
        cursor.close()
        conn.close()
        time.sleep( 1 )
    else:
        logging.info( 'Post time[%s] is not after last time.' % post_create_time_datetime )

    return post


def judge_keywords( title, content, keywords ):

    if keywords == '':
        return True

    keyword_list = keywords.split(',')

    for keyword in keyword_list:

        if keyword in title or keyword in content:
            return True

    return False

def send_email_to_user( posts_to_email, user_email, posts_type, keywords ):

    email_content = ''

    for post in posts_to_email:
        if posts_type == '全部' or posts_type == post.post_type:
            if judge_keywords( post.post_title, post.post_content, keywords ):
                single_post_content = '''<h3><a target="_blank" href=%s>%s</a></h3><p>发表于%s</p><p>%s</p>''' % ( post.post_link, post.post_title, post.post_time, post.post_content )
                email_content += single_post_content
        else:
            logging.info( 'Posts type not match.' )

    if email_content == '':
        logging.info( 'The email content is none.' )
        return
    else:
        sender = configs.email.sender
        receiver = user_email
        subject = configs.email.subject
        smtpserver = configs.email.smtpserver
        smtpport = configs.email.smtpport
        username = configs.email.username
        password = configs.email.password

        msg = MIMEText( email_content,'html','utf-8' )   
        msg['Subject'] = subject  
        msg['From'] = _format_addr('笑然一生 <%s>' % sender)
        msg['To'] = _format_addr('HiPDAer <%s>' % receiver)
        msg['Subject'] = Header('', 'utf-8').encode()

        try:

            smtp = smtplib.SMTP( smtpserver, smtpport )
            smtp.ehlo()
            smtp.starttls()
            smtp.login(username, password)  
            smtp.sendmail(sender, receiver, msg.as_string())  
            smtp.quit()  
        except Exception as e:
            logging.error( 'Send email failed.' )
            logging.exception( e )



if __name__ == '__main__':

    while True:

        # read get_post_time last time from file
        get_post_time_last_time = None
        get_post_time_last_time_stamp = None
        with open('config_get_post_time', 'r') as f:
            get_post_time_last_time = f.read()
        if get_post_time_last_time == '':
            get_post_time_last_time = 0
            get_post_time_last_time_stamp = 0
        else:
            get_post_time_last_time = datetime.strptime( get_post_time_last_time, '%Y-%m-%d %H:%M:%S' )
            get_post_time_last_time_stamp = get_post_time_last_time.timestamp()

        logging.info( '************last time: %s************' % get_post_time_last_time )
        #using cookieJar & HTTPCookieProcessor to automatically handle cookies
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

        pda_url = 'http://www.hi-pda.com/'
        pda_request = HttpRequest( pda_url )
        try:
            pda_request.send_request()
        except TimeoutError:
            logging.warn(" Request url[%s] failed. " % pda_url)
        pda_resp_content = pda_request.get_resp_content()

        formhash_url = 'http://www.hi-pda.com/forum/logging.php?action=login&referer=http%3A//www.hi-pda.com/forum/'
        formhash_request = HttpRequest( formhash_url, None, { 'Host' : 'www.hi-pda.com' } )
        try:
            formhash_request.send_request()
        except TimeoutError:
            logging.warn(" Request url[%s] failed. " % formhash_url)
        formhash_resp_content = formhash_request.get_resp_content()
        try:
            if formhash_resp_content != "":
                formhash_resp_content = formhash_resp_content.decode('gbk')
        except UnicodeDecodeError as e:
            logging.error( 'Decode formhash response content failed.' )
            logging.exception( e )

        # print( formhash_resp_content )
        # <input type="hidden" name="formhash" value="2f68efff" />
        re_formhash = re.compile( r'''<input type="hidden" name="formhash" value="(.+)" />''' )
        formhash = re_formhash.search( formhash_resp_content )
        formhash_content = ''
        if formhash is None:
            logging.warn('Not found the formhash.')
            pass
        else:
            formhash_content = formhash.groups()[0] 

        username = configs.forum.username
        md5 = hashlib.md5()
        password = configs.forum.password
        md5.update( password.encode('utf-8') )
        password = md5.hexdigest()
        
        login_url = 'http://www.hi-pda.com/forum/logging.php?action=login&loginsubmit=yes&inajax=1'
        login_data = {
            'formhash'     : formhash_content,
            'referer'      : 'http://www.hi-pda.com/forum/',
            'loginfield'   : 'username',
            'username'     : username,
            'password'     : password,
            'questionid'   : '0',
            'answer'       : ''
        }
        login_headers = {
            'Referer' : 'http://www.hi-pda.com/forum/logging.php?action=login&referer=http%3A//www.hi-pda.com/forum/',
            'Host'    : 'www.hi-pda.com'
        }
        login_request = HttpRequest( login_url, login_data, login_headers )
        try:
            login_request.send_request()
        except TimeoutError:
            logging.warn(" Request url[%s] failed. " % login_url)
        login_resp_content = login_request.get_resp_content()

        now = datetime.now()
        get_post_time = now.strftime('%Y-%m-%d %H:%M:%S')

        posts_url = 'http://www.hi-pda.com/forum/forumdisplay.php?fid=6'
        posts_headers = {
            'Referer' : 'http://www.hi-pda.com/forum/',
            'Host'    : 'www.hi-pda.com'
        }
        posts_request = HttpRequest( posts_url, None, posts_headers )
        try:
            posts_request.send_request()
        except TimeoutError:
            logging.warn(" Request url[%s] failed. " % posts_url)
        posts_resp_content = posts_request.get_resp_content()
        try:
            if posts_resp_content != "":
                posts_resp_content = posts_resp_content.decode('gbk')
        except UnicodeDecodeError as e:
            logging.error( 'Decode posts response content failed.' )
            logging.exception( e )

        re_pattern = re.compile( r'''<em>\[<a href="forumdisplay\.php\?fid=6&amp;filter=type&amp;typeid=.{1}">(.*)</a>]</em><span id=".*"><a href="(.+?)".*>(.*)</a></span>''' )
        m = re_pattern.findall( posts_resp_content )
        
        posts_to_email = []

        for x in m:
            #print( x )
            post = get_post_content_and_time( x[1], x[0], x[2], get_post_time_last_time_stamp )
            if post is None:
                pass
            else:
                posts_to_email.append( post )
        
        posts_count = len( posts_to_email )
        if 0 == posts_count:
            logging.info( 'There is not new post.' )
        else:
            logging.info( 'There are %s new posts.' % posts_count )

        with open('config_get_post_time', 'w') as f:
            f.write( get_post_time )

        conn = mysql.connector.connect( user = db_user, password = db_passwd, database = db_name )
        cursor = conn.cursor()
        cursor.execute( ' select user_email,posts_type,keywords from push_options where need_push="1" ' )
        result_emails = cursor.fetchall()
        cursor.close()
        conn.close()

        for result_email in result_emails:
            send_email_to_user( posts_to_email, result_email[0], result_email[1], result_email[2] )


        time_interval_dict = configs.time_interval
        current_interval = 480

        hour_now = ( datetime.now() ).hour
        if hour_now in time_interval_dict.keys():
            current_interval = time_interval_dict[hour_now]
        else:
            current_interval = time_interval_dict[-1]

        logging.warn( ' Sleep %s minutes. ' % current_interval )
        time.sleep( current_interval * 60 )


