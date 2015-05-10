"""
    This file contains main()
    Usage:
    
    podderewski command [ optional switches ]
    
    "command" is one, and only one, of the following:
    
    * 'update' to update your feeds' episode lists. May be abbreviated 'up'
    * 'download' to download episodes. May be abbreviated 'dl'
    * 'add' to add a feed
    * 'subscribe' to subscribe to a feed which you've already added
    * 'unsubscribe' to unsubscribe to a feed which you've already added. (The feed will remain on the list,
        and you can subscribe to it again with "podderewski subscribe /feed name/"
    * 'set' to set attributes of a feed
"""

import argparse
from argparse import RawTextHelpFormatter

from service import PodService

"""
    Update episode lists for your subscribed feeds.
    TODO: Make this handle the feeds_to_update list like download() handles
    its list.
"""
def update(feeds_to_update = None):
    feed_list = []
    if feeds_to_update:
        print("Sorry -- this feature not yet implemented.")
        return
    else:
        feed_list = PodService.get_feeds()
    PodService.upate_all_feeds()

"""
    Download episodes for all your subscribed feeds. Set new_only
    to False if you want to re-download episodes that you've already
    gotten. Set overwrite to True if you want to overwrite existing files.
"""
def download(feeds_to_get = None):
    PodService.download(feeds_to_get, overwrite = False, new_only = True)


"""
    Add a feed to our list.
    url: the rss/atom etc url of the feed
    alt_name (optional): the name you want this feed to have in your list. If you don't
        supply this, the name derived by parsing the url will be used.
    episodes_to_keep: the number of episodes you'd like to keep for this feed. If you
        don't supply this, the default value from the configuration file will be used.
        
    After the feed is added, it is not necessary to call subscribe() on it -- it will be
    subscribed as part of the addition process.
"""            
def add(url, alt_name = None, episodes_to_keep = None):
    PodService.add_feed(url,alt_name,episodes_to_keep)

"""
    Subscribe to feeds which you've already added. If you supply a list of names,
    only those feeds will be affected; otherwise all will be subscribed.
"""        
def subscribe(feed_list = None):
    PodService.subscribe(feed_list)
    
"""
    Unsubscribe from feeds which you've already added. If you supply a list of names,
    only those feeds will be affected; otherwise all will be unsubscribed.
"""        
def subscribe(feed_list = None):
    PodService.subscribe(feed_list)
    