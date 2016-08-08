import os
import sys

import pytumblr
from concurrent.futures import ThreadPoolExecutor
from requests_futures.sessions import FuturesSession


class TumblrLikesScraper:

    def __init__(self):
        self.auth_keys = auth_keys = [line.strip() for line in open('oauth_keys.log')]
        self.client = pytumblr.TumblrRestClient(*auth_keys)
        self.num_requests = 0

    def scrape(self, download_fn, finish_fn, offset=0, limit=-1):
        limit_reached = False
        max_throttle = 50
        session = FuturesSession(ThreadPoolExecutor(4))
        total_likes = 0

        likes = self.client.likes(limit=max_throttle, offset=offset)
        while not limit_reached:
            if likes:
                likes = sorted(likes['liked_posts'], lambda a, b: a['liked_timestamp'] < b['liked_timestamp'], reverse=True)
                for like in likes:
                    if limit > -1 and total_likes < limit:
                        limit_reached = True
                        break
                    urls = download_fn(like)
                    if urls:
                        for url in urls:
                            request = session.get(url)
                            request.add_done_callback(lambda f, capture=like: finish_fn(f, capture))
                        total_likes += 1
                likes = self.client.likes(limit=max_throttle, before=likes[-1]['liked_timestamp'])
            else:
                limit_reached = True


def get_like_urls(like_post):
    urls = []
    try:
        if like_post['type'] == 'photo':
            for photo in like_post['photos']:
                if 'original_size' in photo:
                    urls.append(photo['original_size']['url'])
        elif like_post['type'] == 'video':
            if 'video_url' in like_post:
                urls.append(like_post['video_url'])
    except:
        pass
    return urls


def store_media(future, like):
    response = future.result()
    if response and response.ok:
        try:
            if like['type'] == 'photo':
                filename = response.url[response.url.rfind('/')+1:]
                with open(photo_dir + filename, 'w') as f:
                    f.write(response.content)
                    scraped = True
            elif like['type'] == 'video':
                filename = response.url[response.url.rfind('/')+1:]
                with open(video_dir + filename, 'w') as f:
                    f.write(response.content)
                    scraped = True
            if scraped:
                store_media.num_scraped_items += 1
                print '%d scraped items' % store_media.num_scraped_items
        except:
            pass


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Not enough arguments provided'
        exit(1)
    photo_dir = sys.argv[1]
    video_dir = sys.argv[2]
    photo_dir = photo_dir.rstrip('/') + '/'
    video_dir = video_dir.rstrip('/') + '/'
    store_media.num_scraped_items = 0
    if not os.path.isdir(photo_dir):
        os.makedirs(photo_dir)
    if not os.path.isdir(video_dir):
        os.makedirs(video_dir)

    scraper = TumblrLikesScraper()
    scraper.scrape(get_like_urls, store_media)