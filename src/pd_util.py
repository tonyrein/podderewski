from config import PodConfig
import string
import os
import logging


# return codes from command methods:
RET_SUCCESS=0
RET_ARGS_MISSING=1
RET_BAD_ARG_COMBO=2
RET_BAD_ARG_TYPE=3
RET_FILE_NOT_FOUND=4
RET_PERMISSION_ERROR=5
RET_GENERAL_ERROR=6

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

"""
    Given a logging level string such as 'DEBUG' or 'INFO',
    get the corresponding numeric logging level.
"""
def logging_level_from_string(levelstr):
    numeric_level = getattr(logging, levelstr.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % levelstr)
    return numeric_level

"""
    Use the information in the app's configuration
    to set logging options.
"""
def configure_logging():
    cfg = PodConfig.get_instance()
    fn=cfg['main']['log_name']
    levelstr=cfg['main']['log_level']
    if levelstr == '': levelstr = 'NOTSET'
    level = logging_level_from_string(levelstr)
    if fn != 'CONSOLE':
        log_filespec = cfg['main']['log_dir'] + os.sep + fn
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename=log_filespec, level=level)
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=level)
    return logging.getLogger()

    