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
    * 'list' to list feeds
    
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

# return codes from command methods:
RET_SUCCESS=0
RET_ARGS_MISSING=1
RET_BAD_ARG_COMBO=2
RET_BAD_ARG_TYPE=3



"""
    Update episode lists for your subscribed feeds.
    If no list is specified, PodService method will update all subscribed feeds
"""
def update(**kwargs):
    print("Update called")
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    print(feed_list if len(feed_list) > 0  else 'No feeds specified')
    PodService.update_subscribed_feeds(feed_list)
    return RET_SUCCESS

"""
    Download episodes for subscribed feeds.
    Optionally pass a list of feed names; if no list is supplied,
    PodService method will download episodes for all subscribed feeds.
"""
def download(**kwargs):
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    print(feed_list if len(feed_list) > 0  else 'No feeds specified')
    
    PodService.download(feed_list)
    return RET_SUCCESS


"""
    Add a feed to our list.
    url: the rss/atom etc url of the feed
        
    After the feed is added, it is not necessary to call subscribe() on it -- it will be
    subscribed as part of the addition process.
"""            
#def add(url=None):
def add(**kwargs):
    url = kwargs['url'] if 'url' in kwargs else ''
    url = url.strip()
    if url == '':
        print("You must supply the URL of the feed to be added")
        return RET_ARGS_MISSING
    print("Adding " + url)
    #PodService.add_feed(url)
    return RET_SUCCESS

"""
    Subscribe to feeds which you've already added. If you supply a list of names,
    only those feeds will be affected; otherwise all will be subscribed.
"""        
def subscribe(**kwargs):
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    PodService.subscribe(feed_list)
    return RET_SUCCESS
"""
    Unsubscribe from feeds which you've already added. If you supply a list of names,
    only those feeds will be affected; otherwise all will be unsubscribed.
"""        
def unsubscribe(**kwargs):
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    PodService.unsubscribe(feed_list)
    return RET_SUCCESS

"""
    Give a feed a new name.
    Pass the name of the feed, and the new name.
"""
def rename_feed(**kwargs):
    feed_list = kwargs['feeds'] if 'feeds' in kwargs else []
    if len(feed_list) != 1:
        print("The rename command requires exactly one feed name -- none supplied")
        return RET_ARGS_MISSING
    feed_name = feed_list[0]
    new_name = kwargs['newname'] if 'newname' in kwargs else ''
    new_name = new_name.strip()
    if new_name == '':
        print("The rename command requires a new name")
        return RET_ARGS_MISSING
    PodService.rename_feed(feed_name, new_name)
    return RET_SUCCESS

def list_feeds(**kwargs):
    feed_list = PodService.get_feeds()
    if feed_list:
        for feed in feed_list:
            print(feed.name + ": " + ("Subscribed" if feed.is_subscribed else "Not Subscribed") )
    return RET_SUCCESS

"""
    When this feature is implemented it will allow setting
    of features of a Feed. For example:
        set_property('Car Talk', 'keep', 30) to configure this feed
        to retain 30 episodes.
    Here is a list of properties available:
        'keep': number of episodes to keep
        'name': name of the feed. Changing this will also change
            the directory where this episode's feeds are stored - the
            directory will have the same name as the feed.
        'description'
"""
def set_property(feed_list=None,key=None,value=None):
    # Make sure arguments are valid:
    if feed_list is None or key is None or value is None:
        return RET_ARGS_MISSING
    
    if key == 'name':
        # can only have one feed.
        if len(feed_list) != 1:
            return RET_BAD_ARG_COMBO
        feed_name = feed_list[0]
        value = value.strip()
        if value == '': # can't have an empty name
            return RET_ARGS_MISSING
        PodService.rename_feed(feed_name, value)
        return RET_SUCCESS
    
    if key == 'keep':
        # value needs to be an integer
        i = int(value) # Will raise ValueError if string isn't valid integer
        PodService.set_episodes_keep_count(i, feed_list)
        return RET_SUCCESS
    
    if key == 'description':
        PodService.change_feed_description(value, feed_list)
        return RET_SUCCESS
    
    return RET_BAD_ARG_COMBO
        
    
    


def main():
    dispatch_table = {
                  'update': update,
                  'up': update,
                  'download': download,
                  'dl': download,
                  'add': add,
                  'set': set_property,
                  'se': set_property,
                  'subscribe': subscribe,
                  'su': subscribe,
                  'unsubscribe': unsubscribe,
                  'un': unsubscribe,
                  'rename': rename_feed,
                  're': rename_feed,
                  'list': list_feeds,
                  } 
    allowable_commands = [ k for k in dispatch_table ]
    
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('command', choices = allowable_commands,
    help="Allowable commands (you must supply exactly one):\n\n*'update' or 'up' to update feeds\n*'subscribe' or 'unsubscribe' to subscribe\n\tor unsubscribe from feeds\n*'download' or 'dl' to download episodes\n*'add' to add a feed\n*'set' to set feed attributes.")

    parser.add_argument("--feeds", "-f", nargs="*", help="One or more feed names, with each one in quotes", required = False)
    
    parser.add_argument("--value", "-v", help="Value to set for property specified by --property switch",
    required = False)
    
    parser.add_argument("--property", "-p", help="Feed property to change.", required = False)
    
    parser.add_argument("--url", "-u", help = "URL of feed to add.", required = False)
    
    parser.add_argument("--newname", "-n", help="New name for rename command to apply", required = False)

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
    
    