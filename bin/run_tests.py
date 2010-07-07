#!/usr/local/bin/python2.5
import nose, os, sys
from nose.plugins.base import Plugin
from optparse import OptionParser
from gae_path import extend_sys_path, setup_appserver

parser = OptionParser()
parser.add_option("-l", "--logcapture", action="store_true", dest="logcapture")
parser.add_option("--pdb", action="store_true", dest="pdb")
parser.add_option("--pdb-failures", action="store_true", dest="pdb_failures")
(options, args) = parser.parse_args()

test_dir = os.path.join(os.path.dirname(__file__), '../tests')

class TipfyNose(Plugin):
    def configure(self, options, config):
        super(TipfyNose, self).configure(options, config)
        extend_sys_path()
        setup_appserver()

cmdline = [
    '--with-gae',
    '--without-sandbox',
    '--where=' + test_dir,
]

if not options.logcapture:
   cmdline.append('--nologcapture')

if options.pdb_failures:
   cmdline.append('--pdb-failures')

if options.pdb:
   cmdline.append('--pdb')

sys.argv = sys.argv[:1]
nose.main(argv=cmdline, addplugins=[TipfyNose()])

