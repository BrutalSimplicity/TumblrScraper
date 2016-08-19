#Tumblr Scraper (Videos and Post for Likes Only)

I threw this Tumblr Scraper together to grab all of my photos/videos from my likes and save them on my hard drive. You can run this as well, but you'll need to install the PyTumblr package, and create a file called *oauth_keys.log* in the same directory as the script. In that file you will enter your **consumer_key, consumer_secret, oauth_token, and oath_secret** on separate lines and in that order.

```
pip install PyTumblr
```

In the future I would like to add several more features:
- Grab content from your posts and other's posts (if possible)
- Grab content other than photos/video
- Store data in an embedded nosql database like [codernity](http://labs.codernity.com/codernitydb/) so the user can just call an update to grab new content
- more flexible oauth retrieval


## Current Usage

Again, make sure you install `PyTumblr` then just go to the directory and type:

```
python TumblrScraper.py posts videos
```

Where the first argument is the directory for your photos, and the second is for videos.