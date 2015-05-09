from config import PodConfig
import string
import os

# From http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
# method renamed and modified slightly, to substitute '-' for invalid characters.

def remove_invalid_filename_chars(filename):
    validFilenameChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c if c in validFilenameChars else '-' for c in filename)

"""
 Read config - create directories if needed
"""
def init_dirs():
    cfg = PodConfig.get_instance()
    for dir in ( cfg['main']['top_dir'],
                 cfg['main']['log_dir'],
                 cfg['main']['download_dir'],
                 cfg['main']['db_dir'],
                 ):
        if not os.path.isdir(dir):
            os.makedirs(dir) # by default, creates with permissions 0777. Change?
