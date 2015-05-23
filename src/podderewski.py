"""
    This file contains main()
    Usage:
    
    podderewski command [ switches ]
    
    "command" is one, and only one, of the following:
    
    * 'update' to update your feeds' episode lists. May be abbreviated 'up'
    * 'download' to download episodes. May be abbreviated 'dl'
    * 'add' to add a feed
    * 'subscribe' to subscribe to a feed which you've already added. May be abbreviated 'su'
    * 'unsubscribe' to unsubscribe to a feed which you've already added. May be abbreviated 'un' (The feed will remain on the list,
        and you can subscribe to it again with "podderewski subscribe /feed name/"
    * 'set' to set attributes of a feed. May be abbreviated 'se'
    * 'rename' to rename a feed. May be abbreviated 're'
    * 'list' to list feeds. May be abbreviated 'li'. By default includes only subscribed feeds.
    * 'detail' to show detailed information for one or more feeds. May be abbreviated 'de' By default includes only subscribed feeds. 
    
    "switches" are:
    
    * "-f" or "--feeds" -- a list of one or more feed names
    
    * "--url" or "-u" -- URL of a feed
    
    * "--newname" or "-n" -- new name to apply with rename command
    
    * "--property" or "-p" -- name of a feed property. Allowable properties are:
        keep -- number of episodes this feed should keep
        name -- name to use for the feed
        description -- description of feed
        (Note that it makes no sense to give multiple feeds the same name, and
        podderewski will exit with an error message if you ask it to do so.)
        
    * "--value" or "-v" -- value to apply to above property
    
    * "--all" or "-a" -- apply "list" or "detail" command to all feeds, even unsubscribed.
    Examples:
    
    * To update episode lists for all subscribed feeds:
        podderewski up
        
    * To download new episodes for all subscribed feeds:
        podderewski dl
        
    * To update episode lists for only a few feeds:
        podderewski up -f "Car Talk" "Diane Rehm Friday News Roundup" "Linux Luddites"
        
    * To rename a feed:
        podderewski set -f "Diane Rehm Friday News Roundup" -p name -v "News Roundup"
        (Note that if you rename a feed, you also change the location of downloaded episodes.
        The name of the download directory is formed from the feed name.)
        
    * To add a new feed:
        poddereski add "http://www.planetary.org/multimedia/podcasts/planetary-radio-podcast-rss.xml"
        (Note that when the feed is added, it is initially set to "subscribed." You do not need to
        call podderewski subscribe.)
    
        
    Additional arguments for commands:
        * update or download: Optional - name of feed or feeds, if you don't want to apply the command to all feeds.
        * add: Mandatory - URL of feed to add
        * subscribe or unsubscribe: Mandatory - name of feed or feeds
        * set: Mandatory - name of feed or feeds, name of property to set and desired value. For example:
            podderewski set -f "Engines of our Ingenuity" "Car Talk"  -p keep -v 20
            
        Note that in all the above, any feed name containing spaces must be enclosed in single or
        double quotes. Feed lists should be presented like this:
            "Car Talk" "Virtually Speaking Science" 
"""

import argparse
from argparse import RawTextHelpFormatter
import sys

from service import PodService
from dto import Feed, Episode
import pd_util




"""
    Update episode lists for your subscribed feeds.
    If no list is specified, PodService method will update all subscribed feeds
"""
def update(**kwargs):
    print("Update called")
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    if feed_list is None or len(feed_list == 0):
        print("No feeds specified")
    else:
        print(feed_list)
    PodService.update_subscribed_feeds(feed_list)
    return pd_util.RET_SUCCESS

"""
    Download episodes for subscribed feeds.
    Optionally pass a list of feed names; if no list is supplied,
    PodService method will download episodes for all subscribed feeds.
"""
def download(**kwargs):
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    if feed_list is None or len(feed_list == 0):
        print("No feeds specified")
    else:
        print(feed_list)    
    PodService.download(feed_list)
    return pd_util.RET_SUCCESS

    
def _get_feed_detail_string(f):
    pass
# 
# f.name + '\n'
# URL: f.url + '\n'
# f.description
# Last updated f.last_updated.strftime(....)
# Subscribed? Y  Nr. of episodes to keep: 5
# Contains following episodes:
# i = 1
# for e in f.episodes:
#     print(str(i) + '. ' + e + '\n\n')
#     i += 1

"""
    Print detailed information about indicated feed(s).
    If no feed list is supplied, will apply to all subscribed feeds.
    If feed list is supplied, will apply to all subscribed feeds in supplied list.
    To apply to all feeds, subscribed or not, use the "--all" switch. 
"""
def print_feed_detail(**kwargs):
    # First, figure out which feeds this will apply to.
    feeds = []
    # Did caller supply list? If so, use that list; otherwise, use all
    if 'feeds' in kwargs and kwargs['feeds'] is not None and len(kwargs['feeds']) > 0:
        feeds = PodService.feed_list_from_names(kwargs['feeds'])
    else:
        feeds = PodService.get_feeds()
    if feeds:
        do_all = 'all' in kwargs and kwargs['all'] == True
        if do_all == False:
            feeds = [f for f in feeds if f.is_subscribed ]
        for f in feeds:
            self._do_feed_detail(f)
    return pd_util.RET_SUCCESS
"""
    Add a feed to our list.
    url: the rss/atom etc url of the feed
        
    After the feed is added, it is not necessary to call subscribe() on it -- it will be
    subscribed as part of the addition process.
"""            
def add(**kwargs):
    url = kwargs['url'] if 'url' in kwargs else ''
    url = url.strip()
    if url == '':
        print("You must supply the URL of the feed to be added")
        return pd_util.RET_ARGS_MISSING
    print("Adding " + url)
    #PodService.add_feed(url)
    return pd_util.RET_SUCCESS

"""
    Subscribe to feeds which you've already added. If you supply a list of names,
    only those feeds will be affected; otherwise all will be subscribed.
"""        
def subscribe(**kwargs):
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    PodService.subscribe(feed_list)
    return pd_util.RET_SUCCESS
"""
    Unsubscribe from feeds which you've already added. If you supply a list of names,
    only those feeds will be affected; otherwise all will be unsubscribed.
"""        
def unsubscribe(**kwargs):
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    PodService.unsubscribe(feed_list)
    return pd_util.RET_SUCCESS

"""
    Give a feed a new name.
    Pass the current name of the feed, and the new name.
"""
def rename_feed(**kwargs):
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    if feed_list is None or len(feed_list) != 1:
        print("The rename command requires exactly one feed name -- none supplied")
        return pd_util.RET_ARGS_MISSING
    feed_name = feed_list[0]
    new_name = kwargs['newname'] if 'newname' in kwargs else ''
    new_name = new_name.strip()
    if new_name == '':
        print("The rename command requires a new name")
        return pd_util.RET_ARGS_MISSING
    PodService.rename_feed(feed_name, new_name)
    return pd_util.RET_SUCCESS

def describe_feeds(**kwargs):
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    PodService.change_feed_descriptions(feed_list)
    return pd_util.RET_SUCCESS


def list_feeds(**kwargs):
    do_all = 'all' in kwargs and kwargs['all'] == True
    if do_all:
        feed_list = PodService.get_feeds()
    else:
        feed_list = [ f for f in PodService.get_feeds() if f.is_subscribed ]
    if feed_list:
        for feed in feed_list:
            print(feed.name + ": " + ("Subscribed" if feed.is_subscribed else "Not Subscribed") )
    return pd_util.RET_SUCCESS



        
    
    


def main():
    dispatch_table = {
                  'update': update,
                  'up': update,
                  'download': download,
                  'dl': download,
                  'add': add,
                  'subscribe': subscribe,
                  'su': subscribe,
                  'unsubscribe': unsubscribe,
                  'un': unsubscribe,
                  'rename': rename_feed,
                  're': rename_feed,
                  'list': list_feeds,
                  'li': list_feeds,
                  'info': print_feed_detail,
                  'in': print_feed_detail,
                  } 
    allowable_commands = [ k for k in dispatch_table ]
    
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('command', choices = allowable_commands,
    help="Allowable commands (you must supply exactly one):\n\n*'update' or 'up' to update feeds\n*'subscribe' or 'unsubscribe' to subscribe\n\tor unsubscribe from feeds\n*'download' or 'dl' to download episodes\n*'add' to add a feed\n*'info' to show details for one or more feeds.\n*'list' to list feeds.")

    parser.add_argument("--feeds", "-f", nargs="*", help="One or more feed names, with each one in quotes", required = False)
    
    parser.add_argument("--url", "-u", help = "URL of feed to add.", required = False)
    
    parser.add_argument("--newname", "-n", help="New name for rename command to apply", required = False)

    parser.add_argument("--description", "-d", help="New description for feed or list of feeds", required = False)
    
    parser.add_argument("--all", "-a", help='Apply "list" or "detail" command to all feeds, including unsubscribed ones', required=False, action='store_true')
    
    args = parser.parse_args()

    cmd = args.command
    print("Command: " + cmd)
    if not cmd in dispatch_table:
        print(cmd + " is not a valid command")
        sys.exit(1)
        
    PodService.setup()
    retval = dispatch_table[cmd](**vars(args))
    sys.exit(retval)

if __name__ == '__main__':
    main()
    
    