
from dao import FeedDao, EpisodeDao
import pd_util
from config import PodConfig
from peewee import fn

import feedparser
import datetime
import wget
from urlparse import urlparse
import os.path
from operator import attrgetter



# Utility functions:
def create_date_from_structs(published, updated):
    # published and updated are tm_struct structures
    # if updated, use that; otherwise use published
    if updated is not None:
        return datetime.date(updated.tm_year, updated.tm_mon, updated.tm_mday)
    if published is not None:
        return datetime.date(published.tm_year, published.tm_mon, published.tm_mday)
    # if we couldn't find a date, return start of epoch:
    return datetime.date(1970,1,1)

# entry is a feedparser entry object -- one of
# the objects you get by iterating over a parsed feed's entries collection.
def get_entry_url_and_type(entry):
    # Examine the entry's links collection. If there's a link with type 'enclosure,' use
    # that one. Otherwise, if there's a link with type 'alternate,' use that. If neither,
    # return empty strings.
    ret_list = ['','']
    for l in entry.links:
        if l.rel == 'enclosure': # use this one
            return (l.get('href',''),l.get('type',''))
        if l.rel == 'alternate': # save this one -- return it if no 'enclosure' found
            ret_list = [ l.get('href',''), l.get('type','') ]
    return (ret_list[0], ret_list[1])
    
class Feed(object):
    def __init__(self):
        # Derive download directory name and set our property.
        # Property setter creates directory if it isn't already there.
        dir = self.make_download_dir()
        self.download_dir = dir
            
    
    """
        Gets current list of episodes for this feed.
        Then, adds feeds which are not already on this
        feed's episodes list. Sorts list by date and
        retains only specified number of episodes.
    """
    def update(self):
        self.load_episodes_from_db()
        fp = feedparser.parse(self.url)
        if fp and fp.entries:
            for e in fp.entries:
                ep = Episode.create_from_parsed_entry(e)
                if not any(le.episode_id == ep.episode_id for le in self.episodes):
                    # this is a new episode.
                    ep.feed = self
                    ep.dao.feed = self.dao
                    ep.save()
                    self.episodes.append(ep)
        # now sort the episodes list by date, with newest first:
        self.episodes.sort(key=attrgetter('episode_date'), reverse = True)
        # trim the list if there are more episodes than this feed's episodes_to_keep value:
        episodes_to_ditch = self.episodes[self.episodes_to_keep:] # slice will be empty if list shorter than episodes_to_keep
        for ep_to_ditch in episodes_to_ditch:
            ep_to_ditch.delete() 
        self.episodes = self.episodes[0:episodes_to_keep]
        self.last_updated = datetime.datetime.utcnow()
        self.save()

    """
        downloads all episodes which are not already
        in the download directory
    """
    def download_all(self):
        pass
    """
        Where to put downloaded episodes?
        Construct a directory name from the feed name,
        but replace spaces with '_' and characters
        that are not valid in a filename with '-'
    """
    def make_download_dir(self):
        cfg = PodConfig.get_instance()
        n = self.name.replace(' ','_')
        d = pd_util.remove_invalid_filename_chars(n)
        return cfg['main']['top_dir'] + os.sep + cfg['main']['download_dir'] + os.sep + d
    
    """
        download episodes.
        If overwrite is True, download even if episode file already exists. Default is False.
        If new_only is True, do not download episodes that have already been downloaded,
        even if the episode file is no longer there. Default is True.
    """
    def download(self, overwrite = False, new_only = True):
        for ep in self.episodes:
            ep.download(overwrite,new_only)
    
    
    """
        Find episodes in the database which belong to this feed,
        and make Episode instances from them.
    """        
    def load_episodes_from_db(self):
        self.episodes = []
        for ed in self.dao.episodes:
            e = Episode.create_from_dao(ed)
            e.feed = self
            self.episodes.append(e)
    
    """
        Given a FeedDao instance,
        make a Feed.
    """
    @classmethod    
    def create_from_dao(cls,dao):
        f = Feed()
        f.dao = dao
        f.load_episodes_from_db()
        return f
    
    """
        If there's a FeedDao with this name,
        construct a Feed (DTO) and return that.
        The string comparison on the name is
        case-insensitive.
    """
    @classmethod
    def get_feed_by_name(cls,name):
        retf = None
        q = FeedDao.select().where(fn.Upper(FeedDao.name) == name.upper())
        if q.count() == 1:
            retf = Feed.create_from_dao(q.get())
        return retf
    
    """
        Given an url and, optionally, a name, build a Feed
        object.
        
        If alt-name is supplied, use that; otherwise, use the name
        supplied by feedparser.parse(url).
        
        Whichever name is used, see if there's already a Feed by
        that name; if so, return that Feed, and otherwise, build
        a new one.
    """
    @classmethod
    def init_from_url(cls,url,alt_name = None):
        fp = None # Initialize feedparser variable with a null value
        if alt_name is None:
            fp = feedparser.parse(url)
            if fp is None:
                return None
            name = fp.feed.get('title', None)
        else:
            name = alt_name
        if name is None:
            return None
        f = Feed.get_feed_by_name(name)
        if f is None:
            # none by that name -- make a new one:
            fp = fp or feedparser.parse(url)
            if fp is None: return None
            cfg = PodConfig.get_instance()
            f = Feed()
            f.dao = FeedDao()
            f.url = url
            f.name = name
            f.number_to_keep = int(cfg['main']['episodes_to_keep'])
            f.is_subscribed = True
            f.last_updated = datetime.datetime.utcnow()
            f.episodes = []
            f.description = fp.feed.get('description', 'No description found')
            f.save()
            # If any entries, add those to db and to this Feed object's episodes list
            if fp.entries:
                for e in fp.entries:
                    ep = Episode.create_from_parsed_entry(e)
                    ep.feed = f
                    ep.dao.feed = f.dao
                    ep.save()
                    f.episodes.append(ep)
        if alt_name is not None:
            f.name = alt_name
            f.save()
        return f
    

#         If caller DID NOT supply alternate name
#             parse the url and get that name.
#         See if there's already a feed with that name.
#         If so, subscribe to it and return that.
#         Otherwise:
#             create new feed
#             fill in fields
#             fill in episodes
#             return new feed
#     """
#     @classmethod
#     def create_from_url(cls,url):
#         cfg = PodConfig.get_instance()
#         f = Feed()
#         f.dao = FeedDao()
#         f.url = url
#         f.number_to_keep = int(cfg['main']['episodes_to_keep'])
#         f.is_subscribed = True
#         f.last_updated = datetime.datetime.utcnow()
#         f.episodes = []
#         f.__parse_url()
#         return f   
    def save(self):
        self.dao.save()

#     """
#         parse the url. Set the title, date of update and description.
#         Save self.
#         Then, if there are entries:
#             For each entry:
#                 make an Episode
#                 set the Episode's fields
#                 save the Episode
#     """
#     def __parse_url(self):
#         f = feedparser.parse(self.dao.url)
#         if f is not None:
#             self.name = f.feed.get('title', 'No title found')
#             self.description = f.feed.get('description', 'No description found')
#             self.save()
#             
#             if f.entries:
#                 for e in f.entries:
#                     ep = Episode.create_from_parsed_entry(e)
#                     ep.feed = self
#                     ep.dao.feed = self.dao
#                     ep.save()
#                     self.episodes.append(ep)
    
    # Properties -- name, url, description, numbr_to_keep, age_to_keep,
    # is_subscribed, last_updated
    @property
    def name(self):
        return self.dao.name
    @name.setter
    def name(self,newname):
        if newname is None:
            raise Exception('Feed name cannot be null.')
        self.dao.name = newname
    @property
    def url(self):
        return self.dao.url
    @url.setter
    def url(self,newvalue):
        if newvalue is None:
            raise Exception('Feed url cannot be null.')
        self.dao.url = newvalue
    @property
    def description(self):
        return self.dao.description
    @description.setter
    def description(self,newvalue):
        if newvalue is None:
            raise Exception('Feed description cannot be null.')
        self.dao.description = newvalue
    @property
    def number_to_keep(self):
        return self.dao.number_to_keep
    @number_to_keep.setter
    def number_to_keep(self,newvalue):
        if newvalue is None:
            raise Exception('Feed number_to_keep cannot be null.')
        self.dao.number_to_keep = newvalue
    @property
    def is_subscribed(self):
        return self.dao.is_subscribed
    @is_subscribed.setter
    def is_subscribed(self,newvalue):
        if newvalue is None:
            raise Exception('Feed is_subscribed cannot be null.')
        self.dao.is_subscribed = newvalue
    @property
    def last_updated(self):
        return self.dao.last_updated
    @last_updated.setter
    def last_updated(self,newvalue):
        if newvalue is None:
            raise Exception('Feed last_updated cannot be null.')
        self.dao.last_updated = newvalue
    @property
    def download_dir(self):
        return self._download_dir
    @download_dir.setter
    def download_dir(self,newvalue):
        if newvalue is None:
            raise Exception('Feed download_dir cannot be null.')
        self._download_dir = newvalue
        if not os.path.isdir(newvalue):
            os.makedirs(newvalue)



class Episode(object):
    @classmethod
    def create_from_parsed_entry(cls,entry):
        ep = Episode()
        ep.dao = EpisodeDao()
        ep.title = entry.get('title', 'No title found')
        ep.description = entry.get('description', 'No description found')
        ep.episode_id = entry.get('id','')
        ep.episode_date = create_date_from_structs(
            entry.get('published_parsed',None), entry.get('updated_parsed',None))
        ep.downloaded = datetime.date(1970,1,1)
        (ep.url, ep.mime_type) = get_entry_url_and_type(entry)
        return ep
        
    def init_from_parsed_entry(self,entry):
        self.title = entry.get('title', 'No title found')
        self.description = entry.get('description', 'No description found')
        self.episode_id = entry.get('id','')
        self.episode_date = create_date_from_structs(
            entry.get('published_parsed',None), entry.get('updated_parsed',None))
        self.downloaded = datetime.date(1970,1,1)
        (self.url, self.mime_type) = get_entry_url_and_type(entry)
    @classmethod
    def create_from_dao(cls,dao):
        ep = Episode()
        ep.dao = dao
        return ep
        
    def delete(self):
        self.dao.delete_instance()
            
    def save(self):
        self.dao.save()
    
    """
        Use this episode's fields to generate a name of the form
        Description_YYYY-MM-DD.ext, with spaces in description replaced
        by underscores and invalid characters replaced by '-'.
    """    
    def generate_filename(self):
        p = urlparse(self.dao.url).path
        ext = os.path.splitext(p)[1]
        d = self.title.replace(' ','_')
        dtstr = str(self.episode_date.strftime('%Y-%b-%d'))
        return pd_util.remove_invalid_filename_chars(d + '_' + dtstr + ext)
    
    """
        Download this episode.
        If overwrite is True, download even if episode file already exists. Default is False.
        If new_only is True, do not download episodes that have already been downloaded,
        even if the episode file is no longer there. Default is True.
    """
    def download(self, overwrite = False, new_only = True):
        filespec = self.feed.downlad_dir + os.sep + self.generate_filename
        if overwrite == False and os.path.isfile(filespec):
            return ''
        if new_only and self.downloaded != datetime.date(1970,1,1):
            return ''
        dl_res = wget.download(self.url, out=filespec)
        self.downloaded = datetime.datetime.utcnow()
        self.save()
        return dl_res
    
     # Properties
    @property
    def feed(self):
        return self._feed
    @feed.setter
    def feed(self, newvalue):
        if newvalue is None:
            raise Exception("Episode feed cannot be null.")
        self._feed = newvalue
    @property
    def episode_id(self):
        return self.dao.episode_id
    @episode_id.setter
    def episode_id(self, newvalue):
        if newvalue is None:
            raise Exception("Episode id cannot be null.")
        self.dao.episode_id = newvalue
    @property
    def url(self):
        return self.dao.url
    @url.setter
    def url(self, newvalue):
        if newvalue is None:
            raise Exception("Episode url cannot be null.")
        self.dao.url = newvalue
    @property
    def mime_type(self):
        return self.dao.mime_type
    @mime_type.setter
    def mime_type(self, newvalue):
        if newvalue is None:
            raise Exception("Episode mime_type cannot be null.")
        self.dao.mime_type = newvalue
    @property
    def title(self):
        return self.dao.title
    @title.setter
    def title(self, newvalue):
        if newvalue is None:
            raise Exception("Episode title cannot be null.")
        self.dao.title = newvalue
    @property
    def description(self):
        return self.dao.description
    @description.setter
    def description(self, newvalue):
        if newvalue is None:
            raise Exception("Episode description cannot be null.")
        self.dao.description = newvalue
    @property
    def downloaded(self):
        return self.dao.downloaded
    @downloaded.setter
    def downloaded(self, newvalue):
        if newvalue is None:
            raise Exception("Episode downloaded cannot be null.")
        self.dao.downloaded = newvalue
    @property
    def episode_date(self):
        return self.dao.episode_date
    @episode_date.setter
    def episode_date(self, newvalue):
        if newvalue is None:
            raise Exception("Episode episode_date cannot be null.")
        self.dao.episode_date = newvalue
    
    
    
    
    
       