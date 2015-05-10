"""
This package handles interactions with the underlying
sqlite database.


"""
from peewee import *
from config import PodConfig
import os

cfg = PodConfig.get_instance()
_db = SqliteDatabase(cfg['main']['db_dir'] + os.sep + cfg['main']['db_name'])

def init_database():
    _db.connect()
    # Pass True so create call will not throw
    # an exception if tables already exist.
    _db.create_tables([FeedDao,EpisodeDao], True)
    
class BaseModel(Model):
    class Meta:
        database = _db
        
class FeedDao(BaseModel):
    name = CharField()
    url = CharField()
    description = CharField()
    number_to_keep = IntegerField()
    is_subscribed = BooleanField(default=True)
    last_updated = DateTimeField(null=True)
    @classmethod
    def get_feed_dao_by_name(cls,name):
        retd = None
        q = cls.select().where(fn.Upper(cls.name) == name.upper())
        if q.count() == 1:
            retd = q.get()
        return retd
    
        
class EpisodeDao(BaseModel):
    feed = ForeignKeyField(FeedDao, related_name = 'episodes')
    episode_id = CharField()
    url = CharField()
    mime_type = CharField()
    title = CharField()
    description = CharField()
    downloaded = DateTimeField(null=True)
    episode_date = DateTimeField()
    
    
