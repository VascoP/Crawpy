#!/usr/bin/python
from database import *
from settings import *
from sys import argv

def explorer(db):
   counter = 0
   
   while True:
      link = db.get_uncrawled_link()
      if not link:
         if db.is_link_table_empty():
            print "Link table is empty. Costumize \"settings.py\" and run: \"{} --seed\"".format(__file__)
         else:
            db.session.commit()
            print "Crawled {} unexplored links. None available.".format(counter)
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

      # deal with arguments
      if len(argv) > 1:
         if argv[1] == "--seed" or argv[1] == "-s":
            seeds = []
            if len(argv) > 2:
               for i in xrange(2, len(argv)):
                  seeds.append(argv[i])
            db.seed_links(seeds)
            
      explorer(db)
   except KeyboardInterrupt:
      db.session.commit()