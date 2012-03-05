#!/usr/bin/python
from os import path

from sqlalchemy import *
from sqlalchemy.dialects.mysql import LONGTEXT, TINYTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, column_property

from urlparse import urlparse, urljoin

from bs4 import BeautifulSoup as Soup
from bs4 import SoupStrainer

import requests as Reqs

import logging

from settings import *


Base = declarative_base()



class Link(Base):
   # Administrivia
   __tablename__ = 'link'
   pk = Column(Integer, primary_key = True)
   discover_date = Column(DateTime, default=func.now())
   last_seen_date = Column(DateTime, default=func.now(), onupdate=func.now())

   # Juice
   full_url = Column(String(4000, convert_unicode=True))        # Max url said to be 2000 characters
   num_crawls = Column(Integer, default = 0)
   status_code = Column(Integer)
   occurrences = Column(Integer, default = 1)

   #found_at = Column(String(4000, convert_unicode=True))        # Some sort of list?
   #status = Column(TINYTEXT(convert_unicode=True))              # 256 characters ought to be enough

   def __init__(self, url):
      self.full_url = url

   def __repr__(self):
      return "<Link('%s')>" % (self.full_url)

   def crawl(self):
      response = None
      #try:
      response = Reqs.get(self.full_url)
      self.num_crawls += 1
      self.status_code = response.status_code
      #except Reqs.ConnectionError, e:
         #logging.exception(e)      
      return response

   def save(self, db):
      result = db.search_link(self.full_url)
      if result is None:
         db.session.add(self)
      else:
         result.occurrences += 1
         pass

   

class Webpage(Base):
   # Administrivia
   __tablename__ = 'webpage'
   pk = Column(Integer, primary_key = True)
   first_harvest_date = Column(DateTime, default=func.now())
   last_harvest_date = Column(DateTime, default=func.now(), onupdate=func.now())

   # Juice
   full_url = Column(String(4000, convert_unicode=True))     # Max url said to be 2000 characters
   html = Column(LONGTEXT(convert_unicode=True))
   size = Column(Integer)
   num_harvests = Column(Integer, default = 0)
   
   
   def __init__(self, response):
      self.html = response.text
      self.full_url = response.url
      self.size = len(response.text)

   def __repr__(self):
      return "<Webpage('%s')>" % (self.full_url)

   def extract_urls(self):
      url_list = []
      only_a_tags = SoupStrainer("a", href=True)
      
      crawlable = ("http", "https", "")     # Empty scheme meaning relative path
      
      for url in Soup(self.html, parse_only=only_a_tags).find_all("a", href=True):
         url = url.get("href")
         url_scheme = urlparse(url).scheme
         if url_scheme in crawlable:
            # we got a full url here
            if url_scheme:
               url_list.append(url)
            # rebase that shit
            else:
               url_list.append(urljoin(self.full_url, url))
      return url_list

   def save(self, db):
      result = db.search_webpage(self.full_url)
      if result is None:
         db.session.add(self)
         

      

class Database(object):
   session = None
   if DATABASE_PORT:
      db_string = "{}://{}:{}@{}:{}/{}".format(DATABASE_ENGINE, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)
   else:
      db_string = "{}://{}:{}@{}/{}".format(DATABASE_ENGINE, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME)
   
   def __init__(self, db=db_string):
      # Engine and schema creation
      self.engine = create_engine(db, encoding="utf8")
      Base.metadata.create_all(self.engine)
      # Get a session so we can do stuff
      Session = sessionmaker(bind=self.engine)
      self.session = Session()

   def get_uncrawled_link(self):
      return self.session.query(Link).filter(Link.num_crawls == 0).first()

   def get_unharvested_page(self):
      return self.session.query(Webpage).filter(Webpage.num_harvests == 0).first()

   def search_link(self, full_url):
      return self.session.query(Link).filter(Link.full_url == full_url).first()

   def search_webpage(self, full_url):
      return self.session.query(Webpage).filter(Webpage.full_url == full_url).first()
      
   