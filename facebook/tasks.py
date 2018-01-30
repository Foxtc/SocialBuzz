from datetime import datetime
from celery import task
from .models import FacebookNewPage, Post, Person

from fb_scrape_collector.fb_data_collector import FacebookAuthenticator
from fb_scrape_collector.fb_data_collector import FacebookPostsCollector
from fb_scrape_collector.fb_data_collector import FacebookCommentsCollector
#import json, codecs
import sqlite3

@task(name="collect_all_searchs")
def collect_all_searchs():
    search_list = FacebookNewPage.objects.all()
    for search in search_list:
        collect_search.apply_async(args=[search.url])

@task(name="collect_search")
def collect_search(search_url):
    try:
        search = FacebookNewPage.objects.filter(url=search_url)
    except FacebookNewPage.DoesNotExist:
        return
    else:

        url = search[0].url
        app_id = "1113647168736591"
        client_secret = "567c460931e1bbb017932b9361fd877a"
        #show collect from a certain id
        #since_id = search.since_id

        #below, client_id and client_secret should be your actual client ID and secret
        fb_auth = FacebookAuthenticator(app_id,client_secret)
        fb_access_token = fb_auth.request_access_token()

        #to get page posts
        posts_collector = FacebookPostsCollector(fb_access_token)
        posts = posts_collector.collect(url, max_rows=100)

        for item in posts:
            item_object = Post()
            item_object.person = Person()
            if 'from' in item and 'id' in item['from']:
                item_object.person.id = item['from']['id']
            if 'message' in item:
                item_object.message = item['message']
            if 'picture' in item:
                item_object.picture = item['picture']
            if 'link' in item:
                item_object.link = item['link']
            if 'name' in item:
                item_object.name = item['name']
            if 'description' in item:
                item_object.description = item['description']
            if 'type' in item:
                item_object.type = item['type']
            item_object.created_time = item['created_time']
            if 'shares' in item and 'count' in item['shares']:
                item_object.shares = item['shares']['count']
            if 'likes' in item and 'summary' in item['likes'] and 'total_count' in item['likes']['summary']:
                item_object.likes = item['likes']['summary']['total_count']
            if 'LOVE' in item:
                item_object.love = item['LOVE']
            if 'WOW' in item:
                item_object.wow = item['WOW']
            if 'HAHA' in item:
                item_object.haha = item['HAHA']
            if 'SAD' in item:
                item_object.sad = item['SAD']
            if 'ANGRY' in item:
                item_object.angry = item['ANGRY']
            if 'id' in item:
                item_object.id = item['id']
            item_object.person.save()
            item_object.save()

        search[0].pages_count = Post.objects.filter(id=search).count()
        #search.since_id = posts['search_metadata']['max_id']

    return
