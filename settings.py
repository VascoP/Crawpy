import logging
from datetime import date
from requests import defaults as reqsettings


# Number of pages we crawl before commiting to the database
# More is faster but riskier (lose every uncommited crawl on error)
COMMIT_BATCH = 10

# Selected seeds by hand
SEED_LINKS = ["http://www.isup.me/google.com", "http://veja.abril.com.br/", "http://www.stackoverflow.com", "http://dir.yahoo.com/", "http://www.dmoz.org/", "http://www.reddit.com", "http://news.ycombinator.com"]

# Logging level + files
logging.basicConfig(level=logging.DEBUG, filename="logs/connection_errors_{}.log".format(date.today()))

# Settings related to Requests
reqsettings.defaults["base_headers"]["User-Agent"] = "crawpy"
reqsettings.defaults['max_retries'] = 10
reqsettings.defaults['safe_mode'] = True

# Database settings
DATABASE_ENGINE = "mysql"
DATABASE_USER = "root"
DATABASE_PASSWORD = ""
DATABASE_HOST = "localhost"
DATABASE_PORT = ""
DATABASE_NAME = "crawlerdb"