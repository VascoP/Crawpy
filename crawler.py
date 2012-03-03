#!/usr/bin/python
from database import *
import logging
from datetime import date


# Number of pages we crawl before commiting to the database
# More is faster but riskier (lose every uncommited crawl on error)
COMMIT_BATCH = 1

# If each frontier is a level in the webpage graph
# this is how many layers down we will craw on an execution
MAX_DEPTH_GRAPH = 5

# Selected seeds by hand
SEED_LINKS = ["http://www.isup.me/google.com"]#"http://veja.abril.com.br/", "http://www.stackoverflow.com", "http://dir.yahoo.com/", "http://www.dmoz.org/", "http://www.reddit.com", "http://news.ycombinator.com"]

# Number of webpages to select from the database and harvest on each iteration
# higher number means less queries
HARVEST_BATCH = 1

# Logging level + files
logging.basicConfig(level=logging.INFO, filename='logs/connection_errors_{}.log'.format(date.today()))


if __name__ == "__main__":
   frontier = []
   db = Database()

   for i in xrange(MAX_DEPTH_GRAPH):
      # Get the frontier
      results = db.session.query(Webpage).filter(Webpage.num_harvests == 0)[:HARVEST_BATCH]
      
      # Harvest frontier for links
      for result in results:
         frontier += result.extract_links()
         result.num_harvests += 1

      # If there's nothing to harvest (first run, or the last frontier had no new links)
      # we use the seed link set to start crawling
      if not results:
         print "No frontier found. Seeding the crawler."
         frontier = SEED_LINKS

      # Crawl frontier
      for (counter, link) in enumerate(frontier):
         print "[{}/{}] Crawling {}".format(counter+1, len(frontier), link)

         page = None
         attempts = 0   # try 10 times to crawl a page before moving on
         while not page and attempts < 1:
            attempts += 1
            try:
               page = Webpage(link)
            except Reqs.ConnectionError, e:
               logging.exception(e)

         if page:
            page.save_crawl(db)
         
         if counter % COMMIT_BATCH == 0:
            db.session.commit()
      db.session.commit()
      
   





