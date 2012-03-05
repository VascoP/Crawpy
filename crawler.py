#!/usr/bin/python
from database import *
from sys import exit

from settings import *


#def get_path(self):
   #return urlparse(self.full_url).path

#def get_base_url(self):
   #return urljoin(urlparse(self.full_url).scheme, urlparse(self.full_url).netloc)

def main():
   frontier = []
   db = Database()
   max_depth = MAX_DEPTH_GRAPH

   while True:
      # Get the frontier
      results = db.session.query(Webpage).filter(Webpage.num_harvests == 0)[:HARVEST_BATCH]

      if not results:
         # If there's nothing to harvest (first run, or the last frontier had no new links)
         # we use the seed link set to start crawling
         if SEED_LINKS:
            print "No frontier found. Seeding the crawler."
            frontier = SEED_LINKS
         else:
            exit("Empty frontier and no seed links defined. Aborting crawl.")
      else:
         # Harvest frontier for links
         for result in results:
            frontier += result.extract_links()
            result.num_harvests += 1

      

      # Crawl frontier
      for (counter, link) in enumerate(frontier):
         print "[{}/{}] Crawling {}".format(counter+1, len(frontier), link)
         page = Webpage(link)

         if page:
            page.save(db)

         if counter % COMMIT_BATCH == 0:
            db.session.commit()
      db.session.commit()


      # Iteration bounding
      if BOUNDED and max_depth == 0:
         break
      elif BOUNDED:
         max_depth -= 1



if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      pass
      
   





