import os
import sys
 
try:
  sys.path.remove('/usr/lib/python3/dist-packages')
except:
  pass
 
sys.path.append('/home/c/cp46269/django_parser/public_html/')
sys.path.append('/home/c/cp46269/django_parser/myenv/lib/python3.6/site-packages/')
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()