#!/usr/bin/python
from database import *
from settings import *



def explorer(db):
   counter = 0
   
   while True:
      link = db.get_uncrawled_link()
      if not link:
         db.session.commit()
         print "Crawled {} unexplored links. No more available".format(counter)
         break
      response = link.crawl()
      page = Webpage(response)
      page.save(db)

      if counter % COMMIT_BATCH == 0:
         db.session.commit()
      counter += 1



if __name__ == "__main__":
   try:
      db = Database()
      explorer(db)
   except KeyboardInterrupt:
      db.session.commit()