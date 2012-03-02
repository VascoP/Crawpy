#!/usr/bin/python
from database import Database, Webpage


seed_links = ["http://www.isup.me/google.com"]#, "http://www.stackoverflow.com", "http://dir.yahoo.com/", "http://www.dmoz.org/", "http://www.reddit.com", "http://news.ycombinator.com"]
frontier = []

if __name__ == "__main__":
   db = Database()

   # Get the frontier
   results = db.session.query(Webpage).filter(Webpage.num_harvests == 0)[:2]

   # Harvest frontier for links
   for result in results:
      frontier += result.extract_links()
      result.num_harvests += 1

   # If there's nothing to harvest (first run, or the last frontier had no new links)
   # we use the seed link set to start crawling
   if not results:
      print "No frontier found. Seeding the crawler."
      frontier = seed_links

   # Crawl frontier
   for (counter, link) in enumerate(frontier):
      print "[{}/{}] Crawling {}".format(counter+1, len(frontier), link)
      page = Webpage(link)
      page.save_crawl(db)
      if counter % 10 == 0:
         db.session.commit()
   db.session.commit()
      
   





