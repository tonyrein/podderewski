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
        retlist = []
        q = FeedDao.select()
        for fd in q:
            f = Feed.create_from_dao(fd)
            retlist.append(f)
        return retlist
    
    """
        convenience wrapper
    """
    @classmethod
    def get_feed_by_name(cls,name):
        return Feed.get_feed_by_name(name)
#     """
#         If there's a FeedDao with this name,
#         construct a Feed (DTO) and return that.
#         The string comparison on the name is
#         case-insensitive.
#     """
#     @classmethod
#     def get_feed_by_name(cls,name):
#         retf = None
#         q = FeedDao.select().where(fn.Upper(FeedDao.name) == name.upper())
#         if q.count() == 1:
#             retf = Feed.create_from_dao(q.get())
#         return retf
    
    """
        Add a feed, if there isn't already
        one by that name.
    """
    @classmethod
    def add_feed(cls, feed_url, alt_name = None):
        return Feed.init_from_url(feed_url, alt_name)
#         f = Feed.create_from_url(feed_url)
#         if not alt_name is None:
#             f.name = alt_name
#             f.save()

    
    