# socrata-twitterbot

This code expects a local_settings.py (locally) or prod_settings.py (on production server) file in the project directory with a variable called twython_tokens which contains your Twython api tokens, example:


--local_settings.py---

from twython import Twython

twython_tokens = Twython('APP_KEY', 'APP_SECRET',
                  'OAUTH_TOKEN', 'OAUTH_TOKEN_SECRET')
