from datetime import datetime
from celery import task
from .models import FacebookNewPage, Post

from fb_scrape_collector.fb_data_collector import FacebookAuthenticator
from fb_scrape_collector.fb_data_collector import FacebookPostsCollector
from fb_scrape_collector.fb_data_collector import FacebookCommentsCollector
#import json, codecs
import sqlite3

@task(ignore_result=True)
def collect_all_searchs():
    search_list = FacebookNewPage.objects.all()
    for search in search_list:
        collect_search.apply_async(args=[search.id])

@task(ignore_result=True)
def collect_search(search_id):
    try:
        search = FacebookNewPage.objects.get(id=search_id)
    except FacebookNewPage.DoesNotExist:
        return

    url = search.url
    app_id = "1113647168736591"
    client_secret = "567c460931e1bbb017932b9361fd877a"

    #show collect from a certain id
    since_id = search.since_id

    #below, client_id and client_secret should be your actual client ID and secret
    fb_auth = FacebookAuthenticator(app_id,client_secret)
    fb_access_token = fb_auth.request_access_token()

    #to get page posts
    posts_collector = FacebookPostsCollector(fb_access_token)
    posts = posts_collector.collect(url,result_type='recent', count=100, since_id=since_id)

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


    search.created_at = datetime.now()
    search.pages_count = FacebookNewPage.objects.filter(search=search).count()
    search.since_id = posts['search_metadata']['max_id']
    search.save()

    return
