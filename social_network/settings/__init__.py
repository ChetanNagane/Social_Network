import os
import sys

env = os.environ.get('ENVIRONMENT')

if env == 'prod':
    from social_network.settings.prod import *
elif env == 'dev':
    from social_network.settings.dev import *
else:
    sys.stdout.write('using dev settings\n')
    from social_network.settings.dev import *
