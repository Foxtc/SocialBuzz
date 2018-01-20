from fb_data_collector import FacebookAuthenticator
from fb_data_collector import FacebookPostsCollector
from fb_data_collector import FacebookCommentsCollector
import json, codecs
import sqlite3

#below, client_id and client_secret should be your actual client ID and secret
app_id = "1113647168736591"
client_secret = "567c460931e1bbb017932b9361fd877a"

fb_auth = FacebookAuthenticator(app_id,client_secret)
fb_access_token = fb_auth.request_access_token()

#to get page posts
posts_collector = FacebookPostsCollector(fb_access_token)
posts = posts_collector.collect("barackobama",max_rows=100)

#put posts int the db
def sqlite_insert(conn, table, row):
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())
    sql = 'REPLACE INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    conn.cursor().execute(sql, row)
    conn.commit()

conn = sqlite3.connect('../db.sqlite3')

for item in posts:
    #sqlite_insert(conn, item)
    person = item['from']
    del item['from']
    item['person_id'] = person['id']
    if('shares' in item):
        if('count' in item['shares']): item['shares'] = item['shares']['count']
        else: item['shares'] = 0
    item['likes'] = item['likes']['summary']['total_count']
    sqlite_insert(conn,"facebook_person",person)
    sqlite_insert(conn,"facebook_post",item)

#to get comments on a single post
comments_collector = FacebookCommentsCollector(fb_access_token)
post_id = "6815841748_10155375836346749"
comments = comments_collector.collect(post_id,max_rows=100)

#put comments in the db
for item in comments:
    #sqlite_insert(conn, item)
    person = item['from']
    del item['from']
    item['person_id'] = person['id']
    sqlite_insert(conn,"facebook_person",person)
    sqlite_insert(conn,"facebook_comment",item)
