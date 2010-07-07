# -*- coding: utf-8 -*-
import os, sys

bin_dir   = os.path.dirname(__file__)
app_dir   = os.path.abspath(os.path.join(bin_dir, '../app'))
test_dir  = os.path.join(app_dir, '../tests')

app_paths = [ '.', 'lib', 'distlib' ]
app_paths = [os.path.abspath(os.path.join(app_dir, path)) for path in app_paths]
gae_dir   = '/usr/local/google_appengine'
gae_paths = [ '.', 'lib/yaml/lib', 'lib/django', 'lib/antlr3', 'lib/ipaddr', 'lib/webob' ]
gae_paths = [os.path.abspath(os.path.join(gae_dir, path)) for path in gae_paths]

def extend_sys_path():
    sys.path.extend(app_paths + gae_paths)
    
def setup_appserver():
    from google.appengine.tools import dev_appserver
    from google.appengine.tools.dev_appserver_main import ParseArguments
    args, option_dict = ParseArguments(sys.argv) # Otherwise the option_dict isn't populated.
    option_dict['clear_datastore'] = True
    dev_appserver.SetupStubs('local', **option_dict)