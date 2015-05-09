import ConfigParser
import os
import os.path
import sys




class PodConfig(object):
    # Default settings. Note that this is a
    # "static" variable, not tied to any instance.
    _settings = None
    
    @classmethod
    def get_instance(cls):
        if cls._settings is None:
            cls._initialize_settings()
        return cls._settings
    
    @classmethod
    def _initialize_settings(cls):
        def_top_dir = '/opt/podderewski'
        cls._settings = {
                     'main':
                        {
                        'top_dir': def_top_dir,
                        'log_dir': def_top_dir + os.sep + 'logs',
                        'download_dir': def_top_dir + os.sep + 'downloads',
                        'db_type': 'sqlite',
                        'db_dir': def_top_dir + os.sep + 'db',
                        'db_name': 'podderewski.db',
                        'db_host': 'localhost',
                        'db_port': '',
                        'db_user': '',
                        'db_password': '',
                        'log_level': 'WARNING',
                        'log_name': 'CONSOLE',
                        'episodes_to_keep': '30'
                        }
                    }
    

        config_file_search_path = [ '/etc/podderewski.cfg', '/etc/default/podderewski.cfg', '/etc/podderewski/podderewski.cfg',
                        '/usr/local/share/podderewski/podderewski.cfg',  '~/.config/podderewski/podderewski.cfg', './podderewski.cfg']

            
        # See if we can read a config file:
        cfg = ConfigParser.SafeConfigParser()
        cls.config_files_read = cfg.read(config_file_search_path)

        
        # If we found a config file, override
        # defaults with values from config file:
        for section in ['main']:
            if cfg.has_section(section):
                for item in cfg.items(section):
                    cls._settings[section][item[0]] = item[1]

    @classmethod
    def display(cls, *args, **kwargs):
        retStr = ''
        for section in ['main']:
            retStr += '\t' + section + ' section:\n'
            for key in self._settings[section]:
                retStr += '\t\t' + key + ': ' + self._settings[section][key] + '\n'
        return retStr
    

if __name__ == '__main__':
    bc = PDConfig
    if bc.config_files_read is not None and len(bc.config_files_read) > 0:
        print "Read one or more config files: "
        for f in bc.config_files_read: print f
    else:
        print "No config files read; using default values"
    
    print bc
