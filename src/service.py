"""
    The methods in PodService deal primarily with groups of Feed 
"""

from dto import Feed, Episode
from dao import FeedDao, EpisodeDao, init_database
import pd_util

class PodService(object):
    @classmethod
    def setup(cls):
        pd_util.init_dirs()
        init_database() 
    
    
    @classmethod
    def feed_list_from_names(cls, name_list):
        if name_list is None:
            return None
        ret_list = []
        for s in name_list:
            feed = cls.get_feed_by_name(s)
            if feed:
                ret_list.append(feed)
        return ret_list
    """
        Query database and make a FeedDao object for
        each row. Use them to generate a list of Feed (DTO)
        objects and return the list.
    """
    @classmethod
    def get_feeds(cls):
        return Feed.get_feeds()
    
    """
        convenience wrapper
    """
    @classmethod
    def get_feed_by_name(cls,name):
        return Feed.get_feed_by_name(name)

    """
        Get feeds matching arbitrary conditions
        supplied in 'where_clause.'
    """
    @classmethod
    def get_feeds_where(cls, where_clause):
        pass
    
    
    """
        Add a feed, if there isn't already
        one by that name.
    """
    @classmethod
    def add_feed(cls, feed_url, alt_name, episodes_to_keep):
        f = Feed.init_from_url(feed_url, alt_name)
        if episodes_to_keep:
            f.number_to_keep = episodes_to_keep
            f.save()
        return f

    @classmethod
    def update_subscribed_feeds(cls,feeds_to_update = None):
        feed_list = []
        if feeds_to_update is None or len(feed_list) == 0:
            feed_list = cls.get_feeds()
        else:
            feed_list = cls.feed_list_from_names(feeds_to_update)
            
        if feeds_to_update:
            feed_list = cls.feed_list_from_names(feeds_to_update)

        for feed in feed_list:
            if feed.is_subscribed:
                feed.update()
                    
    @classmethod
    def update_all_feeds(cls):
        for feed in cls.get_feeds():
            if feed.is_subscribed:
                feed.update()
    
    """
        Download episodes.
        If overwrite is True, download even if episode file already exists. Default is False.
        If new_only is True, do not download episodes that have already been downloaded,
        even if the episode file is no longer there. Default is True.
        If no feed_list is given, all subscribed feeds will be downloaded. Otherwise,
        get only those subscribed feeds whose names are in feed_list.
    """
    @classmethod
    def download(cls, feed_list, overwrite=False, new_only=True):
        feeds_to_get = []
        if feed_list is None or len(feed_list) == 0:
            feeds_to_get = cls.get_feeds()
        else:
            feeds_to_get = cls.feed_list_from_names(feed_list)
            
        for feed in feeds_to_get:
            if feed.is_subscribed:
                feed.download(overwrite,new_only)
 
    """
        If we were passed a list of feed names, build
        a list of Feed objects from those names. Otherwise,
        just use list of all feeds.
    """
    @classmethod
    def _set_subscribe(cls, state = None, feed_list = None):
        feeds_to_set = []
        if feed_list is None or len(feed_list) == 0: # do all
            feeds_to_set = cls.get_feeds()
        else: # list of names supplied
            feeds_to_set = cls.feed_list_from_names(feed_list)

        for feed in feeds_to_set:
            if feed.is_subscribed != state:
                feed.is_subscribed = state
                feed.save()
    
    """
        For all feeds, or feeds in optional list
        of names, set their is_subscribed state to True.
    """            
    @classmethod
    def subscribe(cls, feed_list = None):
        cls._set_subscribe(True, feed_list)
    
    """
        For all feeds, or feeds in optional list
        of names, set their is_subscribed state to False.
    """
    @classmethod
    def unsubscribe(cls, feed_list = None):
        cls._set_subscribe(False, feed_list)
        
            
    @classmethod
    def rename_feed(cls, feed_name, new_name):
        feed = cls.get_feed_by_name(feed_name)
        if feed:
            feed.name = new_name
            feed.save()
        
    @classmethod
    def set_episodes_keep_count(cls, count, feed_list = None):
        feeds_to_change = []
        if feed_list is None or len(feed_list) == 0:
            feeds_to_change = cls.get_feeds()
        else:
            feeds_to_change = cls.feed_list_from_names(feed_list)
        
        for feed in feeds_to_change:
            feed.number_to_keep = count
            feed.save()
            
    @classmethod
    def change_feed_description(cls, new_description, feed_list = None):
        feeds_to_change = []
        if feed_list is None or len(feed_list) == 0:
            feeds_to_change = cls.get_feeds()
        else:
            feeds_to_change = cls.feed_list_from_names(feed_list)
        
        for feed in feeds_to_change:
            feed.description = new_description
            feed.save()
            
                
                
    