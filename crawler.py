#!/usr/bin/python
from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer

import requests as Reqs

import urlparse

from datetime import datetime

from database import *


seed_links = ("http://www.stackoverflow.com", "http://dir.yahoo.com/", "http://www.dmoz.org/", "http://www.reddit.com", "http://news.ycombinator.com")


def get_page_content(link):
   return Reqs.get(link)

def extract_page_links(link, page_content):
   only_a_tags = SoupStrainer("a", href=True)
   a_tag_list = [(urlparse.urljoin(link, a_tag.get("href")), datetime.now()) for a_tag in Soup(page_content, parse_only=only_a_tags).find_all("a", href=True)]
   return a_tag_list

def save_page(db, response):
   search = db.session.query(Webpage).filter(Webpage.full_url == response.url).first()
   if search is not None:
      search.num_crawls += 1
   else:
      w = Webpage(response.url, response.text)
      db.session.add(w)
   return db


if __name__ == "__main__":
   db = Database()
   
   for link in seed_links:
      response = get_page_content(link)
      save_page(db, response)

   db.session.commit()
      #new_links = extract_page_links(link, page_content)
      #save_page_links(new_links)





