'''
Settings initializer.
'''

import os
from .base import *

if os.environ.get('DJANGO_ENV', None) == 'prod':
    print("Production settings loaded from prod.py file")
elif os.environ.get('DJANGO_ENV', None) == 'test':
    print("test settings loaded from test.py file")
else:
    from .dev import *
    print("development settings loaded from dev.py file")
