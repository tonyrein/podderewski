from dto import Feed, Episode
from dao import FeedDao, EpisodeDao


class PodService(object):
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
        Add a feed, if there isn't already
        one by that name.
    """
    @classmethod
    def add_feed(cls, feed_url, alt_name = None):
        return Feed.init_from_url(feed_url, alt_name)

    @classmethod
    def update_all_feeds(cls):
        for feed in cls.get_feeds():
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
    def download(cls, overwrite = False, new_only = True, feed_list = None):
        if feed_list is None:
            feeds_to_get = cls.get_feeds()
        else:
            feeds_to_get = []
            for name in feed_list:
                f = PodService.get_feed_by_name(name)
                if f:
                    feeds_to_get.append(f)
        for feed in feeds_to_get:
            if feed.is_subscribed:
                feed.download(overwrite,new_only)
                
                
    