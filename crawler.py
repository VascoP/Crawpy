#!/usr/bin/python
from database import Database, Webpage


frontier = seed_links = ("http://www.stackoverflow.com", "http://dir.yahoo.com/", "http://www.dmoz.org/", "http://www.reddit.com", "http://news.ycombinator.com")


if __name__ == "__main__":
   db = Database()
   
   for link in frontier:
      page = Webpage(link)
      page.save_page(db)

   db.session.commit()





