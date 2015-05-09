from dto import *
from dao import *
from service import PodService


# q = FeedDao.select()
# feedlist = []
# for fd in q:
#     f = Feed.create_from_dao(fd)
#     feedlist.append(f)
#     
# f = feedlist[1]
# for e in f.episodes:
#     print(e.generate_filename())
init_database() 
#endao = FeedDao.select().where(FeedDao.name == 'Engines Of Our Ingenuity').get()

sub_urls = [
            ('http://www.npr.org/rss/podcast.php?id=510208','Car Talk'),
            ('http://www.npr.org/rss/podcast.php?id=510030', 'Engines of Our Ingenuity'),
            ('http://thedianerehmshow.org/rss/npr/news_roundup.xml/', 'Diane Rehm Friday News Roundup'),
            ('http://downloads.bbc.co.uk/podcasts/radio4/fricomedy/rss.xml', 'BBC 4 Friday Night Comedy'),
            ('http://feeds.feedburner.com/HistoryExtraPodcast','BBC History Extra'),
            ('http://downloads.bbc.co.uk/podcasts/radio4/ioth/rss.xml', 'In Our Time History Archive'),
            ('http://downloads.bbc.co.uk/podcasts/radio4/iots/rss.xml', 'In Our Time Science Archive'),
            ('http://downloads.bbc.co.uk/podcasts/radio4/timc/rss.xml', 'The Infinite Monkey Cage'),
            ('http://feeds.feedburner.com/LinuxLudditesOgg?format=xml', 'Linux Luddites'),
            ('http://www.planetary.org/multimedia/podcasts/planetary-radio-podcast-rss.xml', 'Planetary Radio'),
            ('http://www.astrosociety.org/edu/podcast/sval.xml', 'Silicon Valley Astronomy Lectures'),
            ('http://www.blogtalkradio.com/virtually-speaking-science/podcast', 'Virtually Speaking Science'),
            ('http://www.npr.org/rss/podcast.php?id=344098539', "Wait Wait Don't Tell Me"),
            ('http://www.pri.org/collections/world-words/feed', 'The World in Words')
            ]

for u in sub_urls:
    PodService.add_feed(u[0], u[1])



#Engines = Feed.create_from_dao(endao)
Engines = PodService.get_feed_by_name('Engines Of Our Ingenuity')
if Engines is not None:
    for ep in Engines.episodes:
        print(ep.feed.get_download_dir() + os.sep + ep.generate_filename())

feedlist = PodService.get_feeds()
for f in feedlist:
    print(f.name)
    
    