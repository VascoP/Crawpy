#!/usr/bin/python
from database import *
from settings import *



def harvester(db):
   counter = 0

   while True:
      page = db.get_unharvested_page()
      if not page:
         db.session.commit()
         print "Harvested {} new webpages. No more available".format(counter)
         break
      url_list = page.extract_urls()
      for url in url_list:
         link = Link(url)
         link.save(db)
      page.num_harvests += 1
      
      if counter % COMMIT_BATCH == 0:
         db.session.commit()
         #pass
      counter += 1



if __name__ == "__main__":
   try:
      db = Database()
      harvester(db)
   except KeyboardInterrupt:
      db.session.commit()