import sae
import sys
import os
from mysite import wsgi

root = os.path.dirname(__file__)
application = sae.create_wsgi_app(wsgi.application)
sys.path.insert(0, os.path.join(root, 'site-packages'))